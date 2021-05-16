from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    name = models.TextField(verbose_name='ingredient_name')
    units = models.TextField(verbose_name='units')

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'name',
                    'units'],
                name='unique ingredient'),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='tagname')
    color = models.CharField(max_length=100, blank=True,
                             verbose_name='tagcolor', default='')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='author')
    title = models.CharField(max_length=64, verbose_name='title')
    image = models.ImageField(blank=True, null=False, verbose_name='image')
    description = models.TextField(verbose_name='description')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='ingredientrecipe')
    tags = models.ManyToManyField(
        Tag, related_name='recipes', verbose_name='tags')
    cooktime = models.PositiveIntegerField(verbose_name='cooktime')
    slug = models.SlugField(verbose_name='slug')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='date'
    )

    def __str__(self):
        return self.title


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='ingredient')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_recipe',
        verbose_name='recipe')
    value = models.PositiveIntegerField(verbose_name='value', null=True)


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='follower')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='following')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'author'],
                name='unique follow'),
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='my_user',
        verbose_name='user')
    recipe = models.ForeignKey(Recipe, blank=True,
                               on_delete=models.CASCADE,
                               related_name='favorite_recipes',
                               default='',
                               verbose_name='favorites')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'],
                name='unique favorite'),
        ]


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_purchases',
        verbose_name='user')
    recipe = models.ForeignKey(
        Recipe, blank=True,
        on_delete=models.CASCADE,
        related_name='listed_recipes',
        default='',
        verbose_name='listed_recipes')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'recipe'],
                name='unique cart'),
        ]
