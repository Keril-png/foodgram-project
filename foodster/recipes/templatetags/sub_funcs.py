from django import template

register = template.Library()


@register.simple_tag
def is_favorite(recipe, user):
    return recipe.favorite.filter(id=user.id).exists()


@register.simple_tag
def is_listed(recipe, user):
    return recipe.in_list.filter(id=user.id).exists()


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
    #Более простого решения через join не смогу придумать... Словарь tags из запроса странно работает, у меня с ним работать здесь не получилось
    path = request.get_full_path()   
    tag_ids = set()
    while 'tag='in path:
        index = path.find('tag=')
        tag_ids.add(int(path[index+4]))
        path = path[:index]+path[index+5:]
    if id in tag_ids:
        tag_ids.remove(id)
    else:
        tag_ids.add(id)
    if path.count('?')==0:
            path+='?'
    while path[-1]!='?':
        path = path[:-1]
    str_tags=[]
    for tag in tag_ids:
        str_tags.append(f"tag={tag}")
    return path+'&'.join(str_tags)
