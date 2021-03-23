from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model() 

class Ingredient(models.Model):
    name = models.TextField() 
    quantity = models.PositiveSmallIntegerField()
    units = models.TextField()

    def __str__(self): 
        return self.name
        
class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.TextField() 
    #image = models.ImageField(blank=True, null=True)
    description = models.TextField() 
    ingredients = models.ManyToManyField(Ingredient)
    #tag = 
    cooktime = models.TimeField()
    slug = models.SlugField()

    def __str__(self): 
        return self.name
    
class Follow(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower") 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following") 