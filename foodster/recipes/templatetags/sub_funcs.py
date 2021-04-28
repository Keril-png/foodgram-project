from django import template
from urllib.parse import urlencode
from recipes.models import Follow, Favorite, Cart

register = template.Library()

@register.simple_tag
def is_favorite(recipe, user):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag
def is_listed(recipe, user):
    return Cart.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag
def listed_count(request):
    return Cart.objects.filter(user=request.user).count()


@register.simple_tag
def other_page(request, page_number):
    path = request.get_full_path()

    this_page = request.GET.get("page")

    if "tag" in path and "page" in path:
        return path.replace(f"page={this_page}", f"page={page_number}")

    if "tag" in path and "page" not in path:
        return path + f"&page={page_number}"
    return f"?page={page_number}"


@register.simple_tag
def tags_filter(request, id, **kwargs):
    path = request.get_full_path()  
    # query = request.GET.copy()
    # query.update(kwargs)
    # return query.urlencode()

    # query['tag'].append[id]
    # ans = query.urlencode()
    # return ans

    # filters = []
    # if query != {}:
    #     for tag in query['tag']:
    #         filters.append(f"tag={tag}")  #Я все еще ищу способ, следующая посылка надеюсь будет нормальной...
    #     string = '&'.join(filters)
    # if path.count('?')==0:
    #         path+='?'
    # while path[-1]!='?':
    #     path = path[:-1]

    # return path+string

    
     
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

@register.simple_tag
def followed(user, author):
    return user.is_authenticated and Follow.objects.filter(
            user=user,
            author=author
        ).exists()
