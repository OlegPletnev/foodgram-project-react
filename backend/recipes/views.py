from config.permissions import IsAuthorOrReadOnly
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.serializers import RecipeMinifiedSerializer
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCart, Tag)
from recipes.serializers import (IngredientSerializer, RecipeSerializer,
                                 TagSerializer)


def delete_method_for_obj(model, user, pk):

    obj = model.objects.filter(user=user, recipe__id=pk)
    if obj.exists():
        obj.delete()
        return Response(
            {'отчет': 'Рецепт успешно удален из списка'},
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        {'errors': 'Ошибка удаления: такого рецепта в вашем списке нет'},
        status=status.HTTP_400_BAD_REQUEST
    )


def post_method_for_obj(model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response(
            {'errors': 'Рецепт уже есть в списке'},
            status=status.HTTP_400_BAD_REQUEST)
    recipe = get_object_or_404(Recipe, id=pk)
    model.objects.create(user=user, recipe=recipe)
    serializer = RecipeMinifiedSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagViewSet(ReadOnlyModelViewSet):
    """
    Вывод списком (list), отвечающих за время приема пищи,
    а также просмотр отдельного тега (retrieve).
    Без фронтенда, без записи, без ограничений в доступе.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Просмотр модели в виде списка или отдельного объекта.
    Без фронтенда, запись только в админке.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    """
    Работа с рецептами. 5 методов.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return RecipeGetSerializer
    #     return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        if request.method == 'POST':
            return post_method_for_obj(Favorite, request.user, pk)
        return delete_method_for_obj(Favorite, request.user, pk)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            return post_method_for_obj(ShoppingCart, request.user, pk)
        return delete_method_for_obj(ShoppingCart, request.user, pk)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__shopping_cart__user=request.user).values(
            'ingredient__name',
            'ingredient__measurement_unit').annotate(total=Sum('amount'))
        shopping_list = 'список:\n'
        for number, ingredient in enumerate(ingredients, start=1):
            shopping_list += (
                f'{number} '
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredient__measurement_unit"]}\n')

        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = ('attachment;'
                                           'filename=purchase_list.txt')
        return response
