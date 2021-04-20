from django.contrib import admin

from .models import Recipe, Ingredient, IngredientRecipe, Follow, Tag


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "units")
    search_fields = ("title",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "color")
    search_fields = ("title",)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "author") 
    search_fields = ("title",) 
    list_filter = ("pub_date",) 
    inlines = (IngredientRecipeInLine, )
    empty_value_display = "-пусто-"


admin.site.register(Ingredient) 
admin.site.register(Recipe, RecipeAdmin) 
admin.site.register(IngredientRecipe) 
admin.site.register(Follow) 
admin.site.register(Tag, TagAdmin) 