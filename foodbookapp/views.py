from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from foodbookapp.models import Recipe
from foodbookapp.forms import UserForm, UserProfileForm, RecipeForm

# Create your views here.

#View for the index page. Defaults to new.
def index(request):
	return new(request)

#View for the /new page
def new(request):
	recipe_list = Recipe.objects.all()
	context_dict = {"recipes": recipe_list}
	return render(request, 'foodbookapp/index.html', context_dict)

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

# View for adding a category
#@login_required
def add_recipe(request):
	form = RecipeForm()

	if request.method == 'POST':
		form = RecipeForm(request.POST)

		if form.is_valid():
			form.save(commit = True)
			return index(request)
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
