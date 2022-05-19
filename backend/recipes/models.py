from django.core import validators
from django.db import models
from users.models import User


class Ingredient(models.Model):
    """
    Таблица ингредиентов, входящих в рецепт по связи Many-to-Many.
    """
    name = models.CharField('Название ингредиента', max_length=200, )
    measurement_unit = models.CharField('Единица измерения', max_length=200, )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique unit',
            ),
        ]

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    """
    Теги. В конкретном проекте - время приема пищи.
    """

    name = models.CharField('Время приема пищи', max_length=200, unique=True, )
    slug = models.SlugField('Слаг', max_length=200, unique=True,)
    color = models.CharField(
        'Цвет в HEX', max_length=7, unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'#[a-f\d]{6}',
                message='Цвет должен быть в HEX кодировке.'
            )
        ]
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Время приема пищи'
        verbose_name_plural = 'Время приемов пищи'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Описание кулинарного рецепта.
    """

    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        error_messages={'unique': 'Такое название рецепта уже существует!'}
    )
    text = models.TextField('Описание',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,)
    image = models.ImageField('Картинка', upload_to='recipes/',)

    cooking_time = models.PositiveSmallIntegerField(
        'Время готовки (мин)',
        validators=[validators.MinValueValidator(
            1,
            message='Минимальное время приготовления 1 минута'
        )
        ]
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Время приема пищи',
        related_name='recipes',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиент с размерностью',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'"{self.name}", автор {self.author}'

    @property
    def get_favourite_count(self):
        """
        У скольких пользователей рецепт находится в избранном.
        """
        return self.favorites.count()

    @property
    def get_ingredients_count(self):
        """
        Сколько ингредиентов в рецепте.
        """
        return self.ingredient_recipe.count()


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='ingredient_recipe'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=(
            validators.MinValueValidator(
                1, message='Количество должно быть >= 1'),)
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient_recipe'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe',),
                name='unique_favorite_recipe',
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепты',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            ),
        )
