from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib.auth.decorators import login_required 
from .models import Recipe, Ingredient, Follow, User, IngredientRecipe, Tag
from django.core.paginator import Paginator 
from django.views.decorators.cache import cache_page 
from .forms import RecipeForm
from django.http import JsonResponse
from .utils import save_recipe
from django.urls import reverse
import json

 
@cache_page(20) 
def index(request): 
    recipe_list = Recipe.objects.order_by('-pub_date').all() 
    tags = set()
    if "tag" in request.GET:
        tags = set(map(int, request.GET.getlist("tag")))
    if tags:
        recipe_list = recipe_list.filter(tags__id__in=tags).distinct()


    paginator = Paginator(recipe_list, 10) 

 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
     
    return render(request, 
        "index.html", 
        { 
            "page": page,  
            'paginator': paginator,
            "all_tags": Tag.objects.all(),
            "tags": tags,
        } 
    ) 

@login_required 
def follow_index(request):
    recipe_list = Recipe.objects.order_by('-pub_date').filter( 
        author__following__user=request.user 
    ) 
    tags = set()
    if "tag" in request.GET:
        tags = set(map(int, request.GET.getlist("tag")))
    if tags:
        recipe_list = recipe_list.filter(tags__id__in=tags).distinct()


    paginator = Paginator(recipe_list, 10) 

 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, 
        "follow.html", 
        { 
            "page": page,  
            'paginator': paginator ,
            "all_tags": Tag.objects.all(),
            "tags": tags,
        } 
    ) 

@login_required 
def favorite(request):
    
    recipe_list = request.user.favorite_recipes.select_related("author",
        ).order_by("-pub_date").all()

    tags = set()
    if "tag" in request.GET:
        tags = set(map(int, request.GET.getlist("tag")))
    if tags:
        recipe_list = recipe_list.filter(tags__id__in=tags).distinct()


    paginator = Paginator(recipe_list, 10) 
 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    return render(request, 
        "favorites.html", 
        { 
            "page": page,  
            'paginator': paginator ,
            "all_tags": Tag.objects.all(),
            "tags": tags,
        } 
    ) 


def ingredients(request):
    name = request.GET['query']
    ingredients = Ingredient.objects.filter(name__istartswith=name).values('name','units')
    return JsonResponse([{"title": ingredient['name'], "dimension": ingredient['units']} for ingredient in ingredients],safe=False)


def author_recipes(request, username):
    author = get_object_or_404(User, username=username)

    recipes = Recipe.objects.select_related(
        "author",
    ).order_by("-pub_date").filter(author=author)

    tags = set()
    if "tag" in request.GET:
        tags = set(map(int, request.GET.getlist("tag")))
    if tags:
        recipes = recipes.filter(tags__id__in=tags).distinct()

    paginator = Paginator(recipes, 10) 

    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 

    following = ( 
        request.user.is_authenticated and Follow.objects.filter( 
            user=request.user,  
            author=author 
        ).exists() 
    ) 

    return render(
        request,
        "author_recipes.html",
        {
            "page": page,
            "paginator": paginator,
            "author": author,
            "all_tags": Tag.objects.all(),
            "tags": tags,
            "following":following,
        }
    )


@login_required
def new_recipe(request):
    if request.method == "POST": 
        form = RecipeForm(request.POST or None, files=request.FILES or None) 
 
        if form.is_valid(): 
            new = save_recipe(request, form)
            return redirect('index') 
        return render(request, 'form_recipe.html', {'form': form}) 
 
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    
    return render(
        request,
        "form_recipe.html",
        {
            "form": form,
        },
    )

@login_required()
def edit_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    url = reverse(
        "single",
        kwargs={"id": id}
    )
    if recipe.author != request.user:
        return redirect(url)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    # if form.is_valid():
    #     recipe.amounts.all().delete()  # clean ingredients before m2m saving
    #     save_form_m2m(request, form)
    #     return redirect(url)
    if form.is_valid(): 
        new = save_recipe(request, form)
        return redirect('index') 
        return render(request, 'form_recipe.html', {'form': form}) 

    used_ingredients = recipe.ingredients.all()
    edit = True

    return render(
        request,
        "form_recipe.html",
        {
            "form": form,
            "used_ingredients": used_ingredients,
            "edit": edit,
        }
    )

@login_required()
def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    url = reverse(
        "index",
    )
    if recipe.author == request.user:
        recipe.delete()
    return redirect(url)


def single_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    amounts = IngredientRecipe.objects.filter(recipe=recipe)
    following = ( 
        request.user.is_authenticated and Follow.objects.filter( 
            user=request.user,  
            author=recipe.author 
        ).exists() 
    ) 

    return render(
        request,
        "single_page.html",
        {   
            "following": following,
            "recipe": recipe,
            "amounts":amounts,
        }
    )


def shoplist(request):
    if request.user.is_authenticated:
        recipes = request.user.listed_recipes.select_related(
            "author",
        ).order_by("-pub_date").all()
        # recipes = Recipe.objects.all()
    else:
        if request.session.get("cart") is not None:
            cart = request.session.get("cart")
        
            recipes = Recipe.objects.filter(id__in=cart)

    return render(
        request,
        "shop_list.html",
        {
            "recipes": recipes,
        }
    )


@login_required 
def profile_follow(request, username): 
    author = get_object_or_404(User, username=username) 
    samefollow = Follow.objects.filter(user=request.user, author=author) 
     
    if request.user != author and not samefollow.exists(): 
        Follow.objects.create( 
            user = request.user, 
            author = author 
        ) 
    return redirect('author_recipes', username=username) 
     
 
 
@login_required 
def profile_unfollow(request, username): 
    author = get_object_or_404(User, username=username) 
    follows = Follow.objects.filter(user = request.user, author = author) 
    if follows.exists(): 
        follows.delete() 
    return redirect('author_recipes', username=username) 


@login_required 
def add_to_favorites(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recipe_id = int(body['id'])
    recipe = get_object_or_404(Recipe, id = recipe_id)
    recipe.favorite.add(request.user)
    return redirect('index')

@login_required 
def remove_from_favorites(request, id):
    recipe = get_object_or_404(Recipe, id = id)
    recipe.favorite.clear()
    return redirect('index')


@login_required 
def add_to_list(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recipe_id = int(body['id'])
    recipe = get_object_or_404(Recipe, id = recipe_id)
    recipe.in_list.add(request.user)
    return redirect('shoplist')

@login_required 
def remove_from_list(request, id):
    recipe = get_object_or_404(Recipe, id = id)
    recipe.in_list.clear()
    return redirect('shoplist')
