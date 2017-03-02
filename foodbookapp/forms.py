from django import forms
from django.contrib.auth.models import User
from foodbookapp.models import Recipe

class RecipeForm(forms.ModelForm):
	maxLengthTitle = Recipe._meta.get_field('title').max_length
	title = forms.CharField(max_length = maxLengthTitle, 
		help_text="Please enter the recipe name.")

	views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	slug = forms.CharField(widget=forms.HiddenInput(), required = False)

	class Meta:
		model = Recipe
		fields = ('name',)

class UserForm(forms.ModelForm):
	password = forms.charField(wiget = forms.PasswordInput())
	picture = forms.ImageField(required=False)

	class Meta(object):
		model = User
		fields = ('username')

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('picture', 'favourites')


