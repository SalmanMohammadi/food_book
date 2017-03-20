import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_book.settings')

import django
django.setup()
from foodbookapp.models import Recipe

def populate():
	cannabis_recipe = {"title": "Cannabis Infused Brownies",
	"views": 100,
	"recipeText": "You need 10 brownes.",
	"pictureLink": "http://i.imgur.com/EacSY7U.gif"}

	cake_recipe = {"title": "simple cake",
	"views": 1200000,
	"recipeText": "You makedeacake.",
	"pictureLink": "http://i.imgur.com/N2C2WFI.gif"}
	
	cake_recipe1 = {"title": "simple cake1",
	"views": 1200000,
	"recipeText": "You makedeacake.",
	"pictureLink": "http://i.imgur.com/N2C2WFI.gif"}
	
	cake_recipe2 = {"title": "simple cake2",
	"views": 1200000,
	"recipeText": "You makedeacake.",
	"pictureLink": "http://i.imgur.com/N2C2WFI.gif"}
	
	cake_recipe3 = {"title": "simple cake3",
	"views": 1200000,
	"recipeText": "You makedeacake.",
	"pictureLink": "http://i.imgur.com/N2C2WFI.gif"}
	
	cake_recipe4 = {"title": "simple cake4",
	"views": 1200000,
	"recipeText": "You makedeacake.",
	"pictureLink": "http://i.imgur.com/N2C2WFI.gif"}
	

	recipes = {"Cannabis Infused Brownies": cannabis_recipe,
				"Cake Recipe": cake_recipe,
				"Cake Recipe1": cake_recipe1,
				"Cake Recipe2": cake_recipe2,
				"Cake Recipe3": cake_recipe3,
				"Cake Recipe4": cake_recipe4,
				}

	for r, recipe_data in recipes.items():
		add_recipe(recipe_data["title"],recipe_data["views"], recipe_data["recipeText"], recipe_data["pictureLink"])

	for r in Recipe.objects.all():
		print((str(r))).encode('utf-8')

def add_recipe(title, views, recipeText, pictureLink):
	r = Recipe.objects.get_or_create(title = title)[0]
	r.views = views
	r.recipeText = recipeText
	r.pictureLink = pictureLink
	r.save()
	return r

#Main method.
if __name__ == '__main__':
	print("Starting FoodBook population script...")
	populate()