from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import SubscribingSerializer


class CustomUserViewSet(UserViewSet):

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        data = Subscribe.objects.filter(user=user, author=author)

        if user == author:
            return Response(
                {'errors': 'Ошибка подписки: Вы с Автором рецептов '
                           'не можете быть одним и тем же лицом'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if data.exists():
            if request.method == 'POST':
                return Response(
                    {'errors': 'Такая подписка уже существует'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            instance = Subscribe.objects.create(user=user, author=author)
            serializer = SubscribingSerializer(
                instance, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Вы не подписаны на этого Автора'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        data_page = self.paginate_queryset(queryset)
        serializer = SubscribingSerializer(
            data_page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
