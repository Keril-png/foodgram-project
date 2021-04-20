from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model() 


class Ingredient(models.Model):
    name = models.TextField() 
    units = models.TextField()

    def __str__(self): 
        return self.name
        

class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name="tagname")
    color = models.CharField(max_length=100, blank=True,
                             verbose_name="tagcolor", default="")


    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length = 64) 
    image = models.ImageField(blank=True, null=True)
    description = models.TextField() 
    ingredients = models.ManyToManyField(Ingredient, through = 'IngredientRecipe')
    tags = models.ManyToManyField(Tag, related_name="recipes")
    cooktime = models.PositiveIntegerField()
    slug = models.SlugField()
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    favorite = models.ManyToManyField(User, blank=True, 
                                      related_name="favorite_recipes")
    in_list = models.ManyToManyField(User, blank=True,
                                    related_name="listed_recipes",
                                    default="")

    def __str__(self): 
        return self.title
    

class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredients") 
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE) 
    value = models.IntegerField()


class Follow(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower") 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following") 
    