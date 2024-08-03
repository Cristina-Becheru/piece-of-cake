from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Recipe

from django import forms
from djrichtextfield.widgets import RichTextWidget  # Adjust import based on your actual setup
from .models import Recipe

class RecipeForm(forms.ModelForm):
    """Form to create a recipe"""

    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "ingredients",
            "instructions",
            "image",
            "image_alt",
            "cake_type",
            "flavor",
            "calories",
            "prep_time",
            "servings",
            "cook_time",
        ]

        widgets = {
            "ingredients": RichTextWidget(),  
            "instructions": RichTextWidget(),  
            "description": forms.Textarea(attrs={"rows": 5}),
            "prep_time": forms.TextInput(attrs={"placeholder": "e.g., 30 minutes"}),  
            "servings": forms.NumberInput(attrs={"placeholder": "e.g., 4 servings"}),  
            "cook_time": forms.TextInput(attrs={"placeholder": "e.g., 45 minutes"}), 
            "calories": forms.NumberInput(attrs={"placeholder": "e.g., 250"}),
        }

        labels = {
            "title": "Recipe Title",
            "description": "Description",
            "ingredients": "Ingredients",
            "instructions": "Instructions",
            "image": "Image",
            "image_alt": "Describe Image",
            "cake_type": "Cake Type",
            "flavor": "Flavor",
            "calories": "Calories",
            "prep_time": "Preparation Time",
            "servings": "Number of Servings",
            "cook_time": "Cooking Time",
        }

    