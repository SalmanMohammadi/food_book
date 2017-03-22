from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from foodbookapp.forms import UserForm, UserProfileForm, RecipeForm, CommentForm, TagForm
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


#View for the home page. Defaults to new.
def home(request, page_name = None):
	try:
		X = 1
	        # get_images()
	except exceptions.RequestException as e:
		print("Unable to connect to api.")
	if(page_name == "new"):
		recipes = Recipe.objects.order_by('submit_date')
	elif(page_name == "trending"):
		recipes = Recipe.objects.order_by('-views')
	else:
		recipes = Recipe.objects.all()

	return render(request, 'foodbookapp/home.html', {'recipes': recipes})

@login_required
def favourited(request):
	error = None
	try:
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
	form = CommentForm()
	tag_form = TagForm()
	context_dict = {}
	context_dict["form"] = CommentForm()
	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
		context_dict['recipe'] = recipe
		context_dict['comments'] = Comment.objects.filter(recipe = recipe)
	except Recipe.DoesNotExist:
		context_dict['recipe'] = None
	except Recipe.comment.DoesNotExist:
		context_dict['comments'] = None

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
			print(request.FILES)
			if 'picture' in request.FILES:
				recipe.picture = request.FILES['picture']
			recipe.save()
			return show_recipe(request, recipe.slug)
		else:
			print(form.errors)

	return render(request, 'foodbookapp/add_recipe.html', {'form': form})

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

@login_required
def fav_recipe(request, type):
	recipe_id = None
	if request.method == 'GET':
		recipe_id = request.GET['recipe_id']
		if recipe_id:
			recipe = Recipe.objects.get(id = int(recipe_id))
			if recipe:
				if type == "true":
					recipe.favourited_by.add(request.user)
					recipe.favourites = recipe.favourites + 1
					recipe.save()
				elif type == "false":
					recipe.favourited_by.remove(request.user)
					recipe.favourites = recipe.favourites - 1
					recipe.save()
	return HttpResponse(recipe.favourites)

def tag_search(request):
	if request.method == 'GET':
	form = SearchForm(data=request.GET)
	if form.is_valid():
		try:
			tags = Recipe.objects.filter(tags=tag_title)
		except Recipe.DoesNotExist:
			tags = None
			error = "Sorry, no recipes with this tag found anything."
	return render(request, 'foodbookapp/home.html', {"recipes": recipes, "error_messages" : error})
			
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required
def user_profile(request):
	context_dict = {}
	try:
		context_dict["recipes"] = Recipe.objects.filter(submitted_by = request.user)
		context_dict["comments"] = Comment.objects.filter(user = request.user)
	except Recipe.DoesNotExist:
		context_dict["recipes"] = none

	return render(request, 'foodbookapp/profile.html', context_dict)

def search(request):
	result_list =[]
	query = ""
	if request.method == 'POST':
		query = request.POST['query'].strip()
		if query:
			# Run our Webhose search function to get the results list!
			result_list = run_query(query)

	return render(request, 'foodbookapp/search.html', {'result_list': result_list, 'query': query})

