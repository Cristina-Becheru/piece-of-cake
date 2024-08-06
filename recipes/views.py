from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    CreateView, ListView,
    DetailView, DeleteView,
    UpdateView
)
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin
)
from django.db.models import Q

from .models import Recipe, Comment, Category
from .forms import RecipeForm, CommentForm

# Define cake types and flavors as constants
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

class RecipeCategoryListView(ListView):
    """View recipes filtered by category"""

    template_name = "recipes/recipes.html"
    context_object_name = "recipes"

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        category = get_object_or_404(Category, slug=category_slug)
        return Recipe.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['selected_category'] = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        context['cake_types'] = dict(CAKE_TYPES)
        context['flavor_types'] = dict(FLAVOR_TYPES)
        return context

class Recipes(ListView):
    """View all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        category_slug = self.request.GET.get('category')
        cake_type_slug = self.request.GET.get('cake_type')
        flavor_slug = self.request.GET.get('flavor')

        recipes = self.model.objects.all()

        if query:
            recipes = recipes.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query)
            )

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            recipes = recipes.filter(category=category)

        if cake_type_slug:
            recipes = recipes.filter(cake_type=cake_type_slug)

        if flavor_slug:
            recipes = recipes.filter(flavor=flavor_slug)

        return recipes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['cake_types'] = dict(CAKE_TYPES)
        context['flavor_types'] = dict(FLAVOR_TYPES)
        return context

class RecipeDetail(DetailView):
    """View a single recipe"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        recipe = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.user = request.user
            comment.save()
            return redirect('recipe_detail', pk=recipe.slug)
        return self.render_to_response(self.get_context_data(comment_form=form))

class AddRecipe(LoginRequiredMixin, CreateView):
    """Add recipe view"""

    template_name = "recipes/add_recipe.html"
    model = Recipe
    form_class = RecipeForm
    success_url = "/recipes/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditRecipe(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit a recipe"""

    template_name = 'recipes/edit_recipe.html'
    model = Recipe
    form_class = RecipeForm
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user

class DeleteRecipe(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a recipe"""

    model = Recipe
    success_url = '/recipes/'

    def test_func(self):
        return self.request.user == self.get_object().user
