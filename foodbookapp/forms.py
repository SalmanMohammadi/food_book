from django import forms
from django.contrib.auth.models import User
from foodbookapp.models import Recipe,UserProfile

class RecipeForm(forms.ModelForm):
	maxLengthTitle = Recipe._meta.get_field('title').max_length
	title = forms.CharField(max_length = maxLengthTitle, 
		help_text="Please enter the recipe name.")

	views = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial = 0)
	
	recipeText = forms.CharField(widget = forms.TextInput(), 
		required=False,help_text = "Please enter the recipe text.")
	picture = forms.ImageField(required=False, help_text = "Upload an image of your recipe.")
	pictureLink = forms.URLField(required=False, help_text = "Submit a url to the image link of.")	

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(RecipeForm, self).__init__(*args, **kwargs)


 	#Ensures a correctly formatted url is passed into the model.
	def clean(self):
		cleaned_data = self.cleaned_data
		pictureLink = cleaned_data.get('pictureLink')
		if pictureLink:
			if not pictureLink.startswith('http://'):
				pictureLink = 'http://' + pictureLink 

			if not pictureLink.endswith('.gif'):
				if pictureLink.endswith('.gifv'):
					pictureLink = pictureLink[:-1]

			cleaned_data['pictureLink'] = pictureLink

		# if self.user:
		# 	cleaned_data['submittedBy'] = self.user.user_profile

		print(cleaned_data)
		return cleaned_data


	class Meta:
		model = Recipe
		exclude = ('slug', 'favouritedBy', 'submittedBy', 'submitDate')

        
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


