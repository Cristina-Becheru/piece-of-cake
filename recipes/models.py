from django.db import models
from django.contrib.auth.models import User

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

    class Meta:
        ordering = ["-posted_date"]

    def __str__(self):
        return str(self.title)
