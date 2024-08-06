from django.contrib import admin
from .models import Recipe, Comment 


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "cake_type",
        "flavor",
        "prep_time",
        "cook_time",
        "servings",
        "calories",
        "posted_date",
        "user",
        "image",
        
    )
    list_filter = ("cake_type", "flavor", "user")
    search_fields = ("title", "description", "ingredients", "instructions")
    ordering = ("-posted_date",)

    # Define the fields to be displayed in the admin form
    fields = (
        "title",
        "user",
        "image",
        "image_alt",
        "description",
        "ingredients",
        "instructions",
        "cake_type",
        "flavor",
        "calories",
        "prep_time",
        "cook_time",
        "servings",
        "posted_date",
        
    )

    readonly_fields = ("posted_date",)
    

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'rating', 'created_at', 'updated_at')
    search_fields = ('user__username', 'recipe__title', 'content')
    list_filter = ('rating', 'created_at', 'updated_at')
    ordering = ('-created_at',)
