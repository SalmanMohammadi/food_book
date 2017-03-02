from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

#View for the index or /foodbook page
def index(request):
	return HttpResponse("FoodBook is LIT!")






