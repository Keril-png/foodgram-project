# Generated by Django 3.2 on 2021-04-24 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0010_auto_20210420_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='following'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='follower'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.TextField(verbose_name='ingredient_name'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='units',
            field=models.TextField(verbose_name='units'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.ingredient', verbose_name='ingredient'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='recipe'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='value',
            field=models.PositiveIntegerField(verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooktime',
            field=models.PositiveIntegerField(verbose_name='cooktime'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='favorites'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='in_list',
            field=models.ManyToManyField(blank=True, default='', related_name='listed_recipes', to=settings.AUTH_USER_MODEL, verbose_name='listed'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(through='recipes.IngredientRecipe', to='recipes.Ingredient', verbose_name='ingredientrecipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.Tag', verbose_name='tags'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='title',
            field=models.CharField(max_length=64, verbose_name='title'),
        ),
    ]
