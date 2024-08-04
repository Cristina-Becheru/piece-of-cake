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

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Recipe, Comment
from .forms import RecipeForm, CommentForm


class Recipes(ListView):
    """View all recipes"""

    template_name = "recipes/recipes.html"
    model = Recipe
    context_object_name = "recipes"

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q')
        if query:
            recipes = self.model.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(instructions__icontains=query) |
                Q(cake_type__icontains=query)
            )
        else:
            recipes = self.model.objects.all()
        return recipes
    


class RecipeDetail(DetailView):
    """View a single recipe"""

    template_name = "recipes/recipe_detail.html"
    model = Recipe
    context_object_name = "recipe"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
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
        return super(AddRecipe, self).form_valid(form)
    
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