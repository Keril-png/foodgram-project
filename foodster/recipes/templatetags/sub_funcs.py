from django import template
from urllib.parse import urlencode
from recipes.models import Follow, Favorite, Cart, Recipe

register = template.Library()


@register.simple_tag
@register.filter
def is_favorite(request, recipe):
    return Favorite.objects.filter(user=request.user, recipe=recipe).exists()


@register.filter
def is_listed(request, recipe):
    return Cart.objects.filter(user=request.user, recipe=recipe).exists()


@register.simple_tag
def listed_count(request):
    return Cart.objects.filter(user=request.user).count()


@register.simple_tag
def author_recipes_left_count(author):
    recipes_count = author.recipes.count() - 3
    if recipes_count % 10 == 1:
        return f'Еще {recipes_count} рецепт...'
    elif recipes_count > 10 and recipes_count < 15:
        return f'Еще {recipes_count} рецептов...'
    elif recipes_count % 10 < 5:
        return f'Еще {recipes_count} рецепта...'
    else:
        return f'Еще {recipes_count} рецептов...'


@register.simple_tag
def other_page(request, page_number):
    path = request.get_full_path()

    this_page = request.GET.get('page')

    if 'tag' in path and 'page' in path:
        return path.replace(f'page={this_page}', f'page={page_number}')

    if 'tag' in path and 'page' not in path:
        return path + f'&page={page_number}'
    return f'?page={page_number}'


@register.filter
def followed(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter(name='tags_filter')
def tags_filter(request, tag):
    new_request = request.GET.copy()
    tags = request.GET.getlist('tag')
    if str(tag) in request.GET.getlist('tag'):
        tags = new_request.getlist('tag')
        tags.remove(str(tag))
        new_request.setlist('tag', tags)
    else:
        new_request.appendlist('tag', tag)
    return new_request.urlencode()
