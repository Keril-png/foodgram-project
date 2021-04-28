from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('new_recipe/', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/', views.single_recipe, name='single'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorite/', views.favorite, name='favorite'),
    path('shoplist/', views.shoplist, name='shoplist'),
    path('shoplist/pdf', views.download_pdf_ingredients, name='get_pdf'),
    path('favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('purchases/', views.add_to_list, name='add_to_list'),
    path('purchases/<int:recipe_id>/', views.remove_from_list, name='remove_from_list'),

    path('<str:username>/', views.author_recipes, name='author_recipes'),
    path('<str:username>/follow/', views.profile_follow, name='profile_follow'),
    path('<str:username>/unfollow/', views.profile_unfollow, name='profile_unfollow'),
]
