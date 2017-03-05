from django import forms
from django.contrib.auth.models import User
from foodbookapp.models import Recipe,UserProfile

class RecipeForm(forms.ModelForm):
	maxLengthTitle = Recipe._meta.get_field('title').max_length
	title = forms.CharField(max_length = maxLengthTitle, 
		help_text="Please enter the recipe name.")

	views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	slug = forms.CharField(widget=forms.HiddenInput(), required = False)
	recipeText = forms.CharField(widget = forms.TextInput())

	class Meta:
		model = Recipe
		fields = ('title',)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta(object):
		model = User
		fields = ('username','password')

class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	class Meta:
		model = UserProfile
		fields = ('picture',) #'favourites' commented out for now


