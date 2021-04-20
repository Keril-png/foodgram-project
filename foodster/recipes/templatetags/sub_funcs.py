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

    if "tags" in path and "page" in path:
        return path.replace(f"page={this_page}", f"page={page_number}")
        
    if "tags" in path and "page" not in path:
        return f"?page={page_number}&{path[2:]}"
    return f"?page={page_number}"
