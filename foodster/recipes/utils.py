from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required 
from .models import Recipe, Ingredient, Follow, User, IngredientRecipe, Tag
from django.core.paginator import Paginator 
from django.views.decorators.cache import cache_page 
from .forms import RecipeForm
from django.http import JsonResponse
import json
from django.db import transaction

from decimal import *

def get_ingredients(request):
    ingredients = {}
    post = request.POST
    for key, name in post.items():
        if key.startswith("nameIngredient"):
            num = key.partition("_")[-1]
            ingredients[name] = post[f'valueIngredient_{num}']
    return ingredients

def save_recipe(request, form):
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()

        objs = []
        ingredients = get_ingredients(request)

        for name, quantity in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)

            objs.append(
                IngredientRecipe(
                    recipe=recipe,
                    ingredient=ingredient,
                    value=Decimal(quantity.replace(',','.'))
                )
            )
        IngredientRecipe.objects.bulk_create(objs)
        form.save_m2m()
        return recipe
