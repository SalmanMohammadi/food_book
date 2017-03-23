from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from foodbookapp.forms import UserForm, UserProfileForm, RecipeForm, CommentForm, TagForm, SearchForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from foodbookapp.models import Recipe, UserProfile, Tag, Comment
from datetime import datetime
from imgurAPI import get_images
from requests import exceptions
from foodbookapp.webhose_search import run_query # searching functionality.
# Create your views here.


#View for the home page. 
def home(request, page_name = None):
	try:
		get_images() #Attempts to retrieve gifs from IMGUR.
	except exceptions.RequestException as e:
		print("Unable to connect to api.")

	#Sorts the recipes depending on whether the user accessed
	# /new, /trending, or /
	if(page_name == "new"):
		#Sorts on submit date, most recent first.
		recipes = Recipe.objects.order_by('-submit_date')
	elif(page_name == "trending"):
		#Sorts on likes, descending.
		recipes = Recipe.objects.order_by('-views')
	else:
		#Sorts on title, alphabetically ascending.
		recipes = Recipe.objects.order_by('title')

	return render(request, 'foodbookapp/home.html', {'recipes': recipes})

#View for /favourited. Only available to logged in users.
@login_required
def favourited(request):
	error = None
	try:
		#Queries the database for all recipes favourited by the user.
		recipes = Recipe.objects.filter(favourited_by=request.user)
	except Recipe.DoesNotExist:
		recipes = None
		error = "You haven't favourited anything."
	return render(request, 'foodbookapp/home.html', {"recipes": recipes, "error_messages" : error})

#View for the /about page.
def about(request):
	return render(request, 'foodbookapp/about.html', {})

#View for the /recipe/<recipe-name> page.
def show_recipe(request, recipe_slug):
	com_form = CommentForm()
	tag_form = TagForm()
	context_dict = {}
	context_dict["comment_form"] = CommentForm()
	context_dict["tag_form"] = TagForm()
	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
		context_dict['recipe'] = recipe
		context_dict['comments'] = Comment.objects.filter(recipe = recipe)
		context_dict['tags'] = recipe.tags
	except Recipe.DoesNotExist:
		context_dict['recipe'] = None
	except Recipe.comment.DoesNotExist:
		context_dict['comments'] = None
	except Recipe.tag.DoesNotExist:
		context_dict['tags'] = None
	return render(request, 'foodbookapp/recipe.html', context_dict)

# View for adding a recipe
@login_required
def add_recipe(request):
	form = RecipeForm()
	if request.method == 'POST':
		form = RecipeForm(data=request.POST)

		if form.is_valid():
			recipe = form.save(commit = False)
			recipe.submitted_by = request.user
			recipe.submit_date = datetime.now()
			if 'picture' in request.FILES:
				recipe.picture = request.FILES['picture']
			recipe.save()
			return show_recipe(request, recipe.slug)
		else:
			print(form.errors)

	return render(request, 'foodbookapp/add_recipe.html', {'form': form})

#View for submitting a comment for a recipe.
@login_required
def add_comment(request, recipe_slug):
	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
	except Recipe.DoesNotExist:
		print("Could not find recipe.")
		return home(request)

	if request.method == 'POST':
		form = CommentForm(data=request.POST)

		if form.is_valid() and recipe:
			comment = form.save(commit = False)
			comment.user = request.user
			comment.recipe = recipe
			comment.save()
		else:
			print(form.errors)

	return show_recipe(request, recipe_slug)

#View for tagging a recipe
@login_required
def add_tag(request, recipe_slug):
	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
	except Recipe.DoesNotExist:
		print("Could not find recipe.")
		return home(request)

	if request.method == 'POST':
		form = TagForm(data=request.POST)
		if form.is_valid() and recipe:
			tag = form.save(commit = False)
			data = form.cleaned_data
			tag, created = Tag.objects.get_or_create(title = data["tag"])
			if created:
				tag.save()
			if tag not in recipe.tags.all():
				recipe.tags.add(tag)
				recipe.save()
		else:
			print(form.errors)

	return show_recipe(request, recipe_slug)	
	
#View for registration, the /register page.
def register(request):
	registered = False
	if request.method =='POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
			messages.add_message(request, messages.ERROR, 'Either the user already exists, or you entered invalid credentials')
			return HttpResponseRedirect(reverse('register'))
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()
	return render(request, 'foodbookapp/register.html',{'user_form':user_form,
														'profile_form': profile_form,
														'registered':registered})

#View for logging a user in.
def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active: # If the account is valid and active, we log the user in.
				login(request, user)
				return HttpResponseRedirect(reverse('home'))
			else:
				# An inactive account was used.
				print("Your account is disabled")
				return HttpResponseRedirect(reverse('login'))
		else: # Bad login details were provided.
			print("Invalid login details: {0}, {1}".format(username, password))
			messages.add_message(request, messages.ERROR, 'Invalid login credentials')
			return HttpResponseRedirect(reverse('login'))
	else:
		return render(request, 'foodbookapp/login.html', {})
	return render(request, 'foodbookapp/login.html', {'dets':'invalid'})

#Handles the AJAX request for a logged in user un/favouriting a recipe.
@login_required
def fav_recipe(request, type):
	recipe_id = None
	if request.method == 'GET':
		recipe_id = request.GET['recipe_id']
		if recipe_id:
			recipe = Recipe.objects.get(id = int(recipe_id))
			if recipe:
				#Favourites the recipe if the AJAX request is for favourite.
				if type == "true":
					recipe.favourited_by.add(request.user)
					recipe.favourites = recipe.favourites + 1
					recipe.save()
				elif type == "false":
				#Unavourites the recipe if the AJAX request is for unfavourite.
					recipe.favourited_by.remove(request.user)
					recipe.favourites = recipe.favourites - 1
					recipe.save()
	return HttpResponse(recipe.favourites)

#Handles searching by tags.
@login_required
def tag_search(request):
	if request.method == 'GET':
		form = SearchForm(data=request.GET)
		recipes = None
		error = None	
		if form.is_valid():
			form.save(commit = False)
			data = form.cleaned_data
			try:
				tag = Tag.objects.get(title=data["tag"])
				recipes = Recipe.objects.filter(tags = tag)
			except Tag.DoesNotExist:
				tag = None
				error = "Sorry, this tag doesn't exist."
			if not recipes:
				recipe = None
				error = "Sorry, this tag has no recipes."
			return render(request, 'foodbookapp/home.html', {"recipes": recipes, "error_messages" : error})
		else:
			print(form.errors)
			return render(request, 'foodbookapp/home.html', {"recipes": recipes, "error_messages" : "form isn't valid"})

#Logs the user out.
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))

#Shows the user profile for a logged in user.
@login_required
def user_profile(request):
	context_dict = {}
	try:
		context_dict["recipes"] = Recipe.objects.filter(submitted_by = request.user)
		context_dict["comments"] = Comment.objects.filter(user = request.user)
	except Recipe.DoesNotExist:
		context_dict["recipes"] = none

	return render(request, 'foodbookapp/profile.html', context_dict)

#Handles searching.
@login_required
def search(request):
	result_list =[]
	query = ""
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			# Run our Webhose search function to get the results list!
			result_list = run_query(query)

	return render(request, 'foodbookapp/search.html', {'result_list': result_list, 'query': query})

