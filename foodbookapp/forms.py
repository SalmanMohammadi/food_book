from django import forms
from django.contrib.auth.models import User
from foodbookapp.models import Recipe, UserProfile, Comment, Tag

#Handles the form for the Recipe model.
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

	#Excludes fields in the form that we want to set in the view.
	class Meta:
		model = Recipe
		exclude = ('favourited_by', 'submitted_by', 'submit_date','tags', 'comments' )

#Handles the form for the Django User model.
class UserForm(forms.ModelForm):
	password = forms.CharField(widget = forms.PasswordInput())

	class Meta(object):
		model = User
		fields = ('username','password')

#Handles the form for the UserProfile model.
class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ('picture',) 

#Handles the form for the Comment model.
class CommentForm(forms.ModelForm):
	body = forms.CharField(help_text = "Submit a comment. Inappropriate comments will be dealt with severely.")
	
	class Meta(object):
		model = Comment
		fields = ('body',)
		
#Handles the form for the Tag model.
class TagForm(forms.ModelForm):
	tag = forms.CharField(help_text = "Tag this recipe.")
	
	class Meta(object):
		model = Tag
		fields = ('tag',)

class SearchForm(forms.ModelForm):
	tag = forms.CharField(help_text = "Find by tag.")
	
	class Meta(object):
		model = Tag
		fields = ('tag',)