import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
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
                    value=Decimal(quantity.replace(',', '.'))
                )
            )
        IngredientRecipe.objects.bulk_create(objs)
        form.save_m2m()
        return recipe

def union_ingredients(request):
    recipes = request.user.listed_recipes.all()
    
    items = IngredientRecipe.objects.filter(recipe__in=recipes)
    combined_ingredients = {}
    for item in items:
        ingredient_name = f"{item.ingredient.name}, {item.ingredient.units}"
        combined_ingredients[ingredient_name] = combined_ingredients.get(
            ingredient_name, 0) + item.value

    return combined_ingredients

def make_pdf(all_ingredients):
    buffer = io.BytesIO()

    needed_ingredients = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    c = 800
    needed_ingredients.setFont("FreeSans", 13)
    for key, value in all_ingredients.items():
        needed_ingredients.drawString(100, c, str(key)+': '+ str(value))
        c-=15

    needed_ingredients.showPage()
    needed_ingredients.save()

    buffer.seek(0)
    return buffer