from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders
import test_utils
# Create your tests here.

class ModelTests(TestCase):

	def setUp(self):
		try:
			from populate_foodbook import populate
			populate()
		except ImportError:
			print('The module populate_rango does not exist')
		except NameError:
			print('The function populate() does not exist or is not correct')
		except:
			print('Something went wrong in the populate() function :-(')
	   
	def get_recipe(self, title):
		from foodbookapp.models import Recipe
		try:				  
			recipe = Recipe.objects.get(title=title)
		except Recipe.DoesNotExist:	   
			recipe = None
		return recipe

	def test_cannabis_added(self):
		recipe = self.get_recipe('Cannabis Infused Brownies')  
		self.assertIsNotNone(recipe)
		 
	def test_python_cat_with_views(self):
		cat = self.get_category('Python')
		self.assertEquals(cat.views, 128)
		
	def test_url_reference_in_index_page_when_logged(self):
		# Create user and log in
		test_utils.create_user()
		self.client.login(username='testuser', password='test1234')

		# Access index page
		response = self.client.get(reverse('home'))

		# Check links that appear for logged person only
		self.assertIn(reverse('home'), response.content)
		self.assertIn(reverse('favourited'), response.content)
		self.assertIn(reverse('about'), response.content)
		self.assertIn(reverse('logout'), response.content)
		self.assertIn(reverse('profile'), response.content)
		