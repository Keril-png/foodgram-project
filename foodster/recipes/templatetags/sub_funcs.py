from django import template

register = template.Library()


@register.simple_tag
def is_favorite(recipe, user):
    return recipe.favorite.filter(id=user.id).exists()


@register.simple_tag
def is_listed(recipe, user):
    return recipe.in_list.filter(id=user.id).exists()


@register.simple_tag
def is_in_session_cart(request, product_id):
    cart = request.session.get("cart")
    if cart is not None:
        if product_id in cart:
            return True
    return False


@register.simple_tag
def listed_count(request):
    return request.user.listed_recipes.count()


@register.simple_tag
def other_page(request, page_number):
    path = request.get_full_path()

    this_page = request.GET.get("page")

    if "tag" in path and "page" in path:
        return path.replace(f"page={this_page}", f"page={page_number}")

    if "tag" in path and not ("page" in path):
        return path + f"&page={page_number}"
    return f"?page={page_number}"


@register.simple_tag
def tags_filter(request, id):
    path = request.get_full_path()
    if f'&tag={id}' in path:
        return path.replace(f"&tag={id}", "")
    elif f'tag={id}&' in path:
        return path.replace(f"tag={id}&", "")
    elif f'tag={id}' in path:
        return path.replace(f"tag={id}", "")
    elif path.count('tag') > 0:
        return path + f'&tag={id}'
    else:
        return path + f'?tag={id}'
