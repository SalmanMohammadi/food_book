from django import forms
from django.contrib.auth.models import User
from foodbookapp.models import Recipe, UserProfile, Comment, Tag

class RecipeForm(forms.ModelForm):
	maxLengthTitle = Recipe._meta.get_field('title').max_length
	title = forms.CharField(max_length = maxLengthTitle, 
		help_text="Please enter the recipe name.")

	views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	favourites = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)
	recipe_text = forms.CharField(widget = forms.TextInput(), 
		required=False,help_text = "Please enter the recipe text.")

	picture = forms.ImageField(required=False, help_text = "Upload an image of your recipe.")
	picture_link = forms.URLField(required=False, help_text = "Submit a url to the image link.")	

 	#Ensures a correctly formatted url is passed into the model.
	def clean(self):
		cleaned_data = self.cleaned_data
		pictureLink = cleaned_data.get('pictureLink')
		if pictureLink:
			if not pictureLink.startswith('http://'):
				pictureLink = 'http://' + pictureLink 

			if not pictureLink.endswith('.gif'):
				if spictureLink.endswith('.gifv'):
					pictureLink = pictureLink[:-1]

			cleaned_data['pictureLink'] = pictureLink

		return cleaned_data

	class Meta:
		model = Recipe
		exclude = ('favourited_by', 'submitted_by', 'submit_date','tags', 'comments' )

class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta(object):
		model = User
		fields = ('username','password')

class UserProfileForm(forms.ModelForm):
	picture = forms.ImageField(required=False)
	class Meta:
		model = UserProfile
		fields = ('picture',) 

class CommentForm(forms.ModelForm):
	comment = forms.CharField(min_length=10)
	
	class Meta(object):
		model = Comment
		fields = ('comment',)
		
class TagForm(forms.ModelForm):
	tag = forms.CharField(min_length=3)
	
	class Meta(object):
		model = Tag
		fields = ('tag',)
