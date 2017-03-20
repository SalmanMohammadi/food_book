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
# Create your views here.

#View for the home page. Defaults to new.
def home(request, page_name = None):
	try:
		x=1
		# get_images()
	except:
		print("Unable to connect to API.")
	print(page_name)
	# if(page_name == "new"):
	# 	recipes = Recipe.objects.sort()
	# else if(page_name == "trending"):
	# 	recipes = Recipe.objects.sort()
	# else if(page_name == "favourited"):
	# 	recipes = Recipe.objects.sort()
	recipes = Recipe.objects.all()
	return render(request, 'foodbookapp/home.html', {'recipes': recipes})

@login_required
def favourited(request):
	home(request, "favourited")

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

		
		#try:
			# tags = Tag.objects.get(recipe = recipe.id)
		# except Tag.DoesNotExist:
			# context_dict['tags'] = None	
	
# View for adding a recipe
@login_required
def add_recipe(request):
	form = RecipeForm()
	if request.method == 'POST':
		form = RecipeForm(data=request.POST)

		if form.is_valid():
			form.save(commit = False)
			data = form.cleaned_data
			try: 
				rec1 = Recipe.objects.get(title = data["title"]) 
				rec2 = Recipe.objects.get(recipe_text = data["recipe_text"]) 
				rec3 = Recipe.objects.get(picture_link = data["picture_link"])
				rec4 = Recipe.objects.get(picture = data["picture"])
			except Recipe.DoesNotExist:
				recipe = Recipe.objects.get_or_create(title = data["title"],
					views = data["views"], recipe_text = data["recipe_text"],
					picture = data["picture"], picture_link = data["picture_link"],
					submitted_by = request.user, submit_date = datetime.now())[0]
				recipe.save()
				return show_recipe(request, recipe.slug)
			except Recipe.MultipleObjectsReturned:
				messages.add_message(request, messages.ERROR, 'A part of this recipe already exists in our database')
			print(form.errors)	
		else:
			print(form.errors)

	return render(request, 'foodbookapp/add_recipe.html', {'form': form})

@login_required	
def update_rating(request):
	rec_id = request.POST.get('rec_id',False)
	if rec_id:
		rec = Recipe.objects.get(recipe_id=rec_id)
		rs = rec.raters #raters
		rs = rs + 1
		rec.raters = rs
		rec.score = 1.0 #score
		rec.save()	
		#Algorithm to update the ratings
		# raters = theRecipe.raters
		# score = theRecipe.score
		# score = score * raters
		# score + request.POST["score"]
		# raters+=1
		# score = score/raters
		#Algorithm end
	return HttpResponse(rec);
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
		return render(request, 'foodbookapp/login.html', {'dets':'invalid'})

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required
def user_profile(request):
	return render(request, 'foodbookapp/profile.html', {})
