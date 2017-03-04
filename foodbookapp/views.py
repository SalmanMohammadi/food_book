from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from foodbookapp.models import Recipe

# Create your views here.

#View for the index /new page
def new(request):
	recipe_list = Recipe.objects.all()
	context_dict = {"recipes": recipe_list}
	return render(request, 'foodbookapp/index.html', context_dict)

def about(request):
	return render(request, 'foodbookapp/about.html', {})

def show_recipe(request):
	context_dict = {}

	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
		context_dict['recipes'] = recipe
	except Recipe.DoesNotExist:
		context_dict['recipe'] = None

	return render(request, 'foodbookapp/recipe.html', context_dict)
