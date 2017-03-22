from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.staticfiles import finders

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