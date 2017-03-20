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
# Create your views here.


#View for the home page. Defaults to new.
def home(request, page_name = None):
	try:
		X = 1
		# get_images()
	except exceptions.RequestException as e:
		print("unable to connect to api.")

	if(page_name == "new"):
		print(page_name)
		recipes = Recipe.objects.order_by('submit_date')
	elif(page_name == "trending"):
		recipes = Recipe.objects.order_by('-views')
	else:
		print("none")
		recipes = Recipe.objects.all()

	print(Recipe.objects.order_by('submit_date'))
	print("all")
	print(Recipe.objects.all())
	print(recipes)
	return render(request, 'foodbookapp/home.html', {'recipes': recipes})

@login_required
def favourited(request):
	print(request.user)
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
	com_form = CommentForm()
	tag_form = TagForm()
	context_dict = {}
	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
		context_dict['recipe'] = recipe
		context_dict['comments'] = Comment.objects.filter(com_recipe = recipe)
	#DISPLAY ALL COMMENTS
	except Recipe.DoesNotExist:
		context_dict['recipe'] = None
	context_dict["user"] = request.user
	
	#if we have a recipe and post a comment/tag
	if context_dict['recipe'] != None:
		if request.method == 'POST' and 'com_form' in request.POST:
			com_form = CommentForm(data=request.POST)
			if com_form.is_valid():
				com_form.save(commit = False)
				data = com_form.cleaned_data
				comment, created = Comment.objects.get_or_create(com_body = data["comment"], com_recipe = recipe, com_user = request.user)
				comment.save()
				request.method = 'GET'
				return show_recipe(request, recipe.slug)
			else:
				print(com_form.errors)
		if request.method == 'POST' and 'tag_form' in request.POST:
			tag_form = TagForm(data=request.POST)
			if tag_form.is_valid():
				tag_form.save(commit = False)
				data = tag_form.cleaned_data
				tag, created = Tag.objects.get_or_create(tagTitle = data["tag"])
				tag.save()
				if tag not in recipe.tags.all():
					recipe.tags.add(tag)
					recipe.save()
				request.method = 'GET'
				return show_recipe(request, recipe.slug)
			else:
				print(tag_form.errors)
	return render(request, 'foodbookapp/recipe.html', context_dict)
	
# View for adding a recipe
@login_required
def add_recipe(request):
	form = RecipeForm()
	if request.method == 'POST':
		form = RecipeForm(data=request.POST)

		if form.is_valid():
			recipe = form.save(commit = False)
			data = form.cleaned_data
			recipe.submitted_by = request.user
			recipe.submit_date = datetime.now()
			recipe.save()
			return show_recipe(request, recipe.recipe_slug)
		else:
			print(form.errors)
	return render(request, 'foodbookapp/add_recipe.html', {'form': form})

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
			if 'Picture' in request.FILES:
				profile.picture = request.FILES['Picture']
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)
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


@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required
def user_profile(request):
	return render(request, 'foodbookapp/profile.html', {})

