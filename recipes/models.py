from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from djrichtextfield.models import RichTextField
from django_resized import ResizedImageField

CAKE_TYPES = [
    ("classic", "Classic"),
    ("fruit", "Fruit Cake"),
    ("cupcake", "Cupcake"),
    ("cheesecake", "Cheesecake"),
]

FLAVOR_TYPES = [
    ("vanilla", "Vanilla"),
    ("chocolate", "Chocolate"),
    ("strawberry", "Strawberry"),
    ("lemon", "Lemon"),
    ("coffee", "Coffee"),
]

class Category(models.Model):
    """Model to represent a category with subcategories"""
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[('cake', 'Cake'), ('flavor', 'Flavor')], blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    

class Recipe(models.Model):
    """
    A model to create and manage cake recipes
    """

    user = models.ForeignKey(
        User, related_name="cake_recipes", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=300, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    ingredients = RichTextField(max_length=10000, null=False, blank=False)
    instructions = RichTextField(max_length=10000, null=False, blank=False)

    image = ResizedImageField(
        size=[400, None],
        quality=75,
        upload_to="recipes/",
        force_format="WEBP",
        blank=False,
        null=False,
    )
    image_alt = models.CharField(max_length=100, null=False, blank=False)
    cake_type = models.CharField(max_length=50, choices=CAKE_TYPES, default="classic")
    flavor = models.CharField(max_length=50, choices=FLAVOR_TYPES, default="vanilla")
    calories = models.PositiveIntegerField()
    prep_time = models.CharField(max_length=50, null=True, blank=True)
    cook_time = models.CharField(max_length=50, null=True, blank=True)
    servings = models.PositiveIntegerField()
    posted_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, related_name="cakes", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    """
    A model to create and manage comments on recipes
    """
    user = models.ForeignKey(
        User, related_name="recipe_comments", on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField(null=False, blank=False)
    rating = models.PositiveIntegerField(choices=[(i, f"{i} Star") for i in range(1, 6)], default=5)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.username} on {self.recipe.title}"