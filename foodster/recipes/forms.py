from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        
    class Meta:
        model = Recipe
        fields = ('title', 'tags', 'cooktime', 'description', 'image',)

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
