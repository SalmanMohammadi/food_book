from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from foodbookapp.models import Recipe

# Create your views here.

#View for the index or /foodbook page
def index(request):
	recipe_list = Recipe.objects.all()
	context_dict = {"recipes": recipe_list}
	return render(request, 'foodbookapp/index.html', context_dict)


def new(request):
	return HttpResponse("FoodBook is LIT!")




