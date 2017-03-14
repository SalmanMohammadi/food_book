from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from foodbookapp.forms import UserForm, UserProfileForm, RecipeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from foodbookapp.models import Recipe, UserProfile
from datetime import datetime
# Create your views here.

#View for the index page. Defaults to new.
def home(request):
	recipes = Recipe.objects.all()
	return render(request, 'foodbookapp/home.html', {'recipes': recipes})
	#return new(request)

#View for the new page
def new(request):
	recipes = Recipe.objects.all()
	return render(request, 'foodbookapp/new.html', {'recipes': recipes})

#View for the /about page.
def about(request):
	return render(request, 'foodbookapp/about.html', {})

#View for the /recipe/<recipe-name> page.
def show_recipe(request, recipe_slug):
	context_dict = {}
	try:
		recipe = Recipe.objects.get(slug = recipe_slug)
		context_dict['recipe'] = recipe
	except Recipe.DoesNotExist:
		context_dict['recipe'] = None

	return render(request, 'foodbookapp/recipe.html', context_dict)

# View for adding a recipe
@login_required
def add_recipe(request):
	form = RecipeForm()
	if request.method == 'POST':
		form = RecipeForm(data=request.POST)

		if form.is_valid():
			form.save(commit = False)
			data = form.cleaned_data
			recipe = Recipe.objects.get_or_create(title = data["title"],
				views = data["views"], recipeText = data["recipeText"],
				picture = data["picture"], pictureLink = data["pictureLink"],
				submittedBy = request.user, submitDate = datetime.now())[0]
			recipe.save()
			return show_recipe(request, recipe.recipe_slug)
		else:
			print(form.errors)

	return render(request, 'foodbookapp/add_recipe.html', {'form': form})

@login_required	
def update_rating(request):
	rec_id = request.POST["rec_id"]
	rec = Recipe.objects.get(id=int(rec_id))
	rec.raters = 500 #raters
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
	return HttpResponse("Update successful!")

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
				return HttpResponse("Your account is disabled.")
		else: # Bad login details were provided. 
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
	else:
		return render(request, 'foodbookapp/login.html', {})

def trending(request):
	
	
	return render(request, 'foodbookapp/trending.html')

def favourited(request):
	
	
	return render(request, 'foodbookapp/favourited.html')		

@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	return HttpResponseRedirect(reverse('home'))

@login_required
def user_profile(request):
	return render(request, 'foodbookapp/profile.html', {})
