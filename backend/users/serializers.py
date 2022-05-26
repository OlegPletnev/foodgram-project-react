from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe
from .models import Subscribe, User


class RecipeMinifiedSerializer(ModelSerializer):
    """
    Укороченный (минифицированный) набор полей для модели Recipe.
    Используется в некоторых эндпоинтах-списках.
    """

    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
        read_only_fields = ('id', 'name', 'image', 'cooking_time',)


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Используется при регистрации пользователя.
    """

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}, }
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class CustomUserSerializer(UserSerializer):
    """
    Информация об авторе. Используется в некоторых ответах на запрос.
    """

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        """
        Подписан ли текущий пользователь на просматриваемого.
        """

        user = self.context.get('request').user
        if user.is_authenticated and (user != obj):
            return Subscribe.objects.filter(user=user, author=obj).exists()
        return False


class SubscribingSerializer(CustomUserSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='author.recipes.count',
        read_only=True
    )

    class Meta:
        model = Subscribe
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count',)

    def get_is_subscribed(self, obj):
        """
        Избыточное поле по условию задания.
        Всегда True.
        """
        return True

    def get_recipes(self, obj):
        """
        Параметр запроса (QUERY PARAMETERS) recipes_limit
        ограничивает кол-во объектов внутри поля recipes.
        """
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.author)
        if limit:
            queryset = queryset[:int(limit)]
        return RecipeMinifiedSerializer(queryset, many=True).data
