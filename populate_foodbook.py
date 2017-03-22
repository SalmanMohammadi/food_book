import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_book.settings')

import django
django.setup()
from foodbookapp.models import Recipe, User, Comment
from datetime import datetime

def populate():
	cannabis_recipe = {"title": "Cannabis Infused Brownies",
	"views": 100,
	"favourites": 0,
	"submit_date": datetime.now(),
	"recipeText": "You need 10 brownes.",
	"pictureLink": "http://i.imgur.com/EacSY7U.gif",
	"comments": ["This is the dankest **** I've ever tried! xD",
				"Weed is for losers.",
				"4200000000000 life!"]}

	cake_recipe = {"title": "simple cake",
	"views": 1200000,
	"favourites": 0,
	"submit_date": datetime.now(),
	"recipeText": "You makedeacake.",
	"pictureLink": "http://i.imgur.com/N2C2WFI.gif",
	"comments": ["My mom doesn't love me.",
				"Who gives a **** about your mom? LOSER",
				"I give a **** about his mom XD lel"]}

	recipes = {"Cannabis Infused Brownies": cannabis_recipe,
				"Cake Recipe": cake_recipe,
				}

	for r, recipe_data in recipes.items():
		add_recipe(recipe_data["title"],recipe_data["views"], 
			recipe_data["recipeText"], recipe_data["pictureLink"],
			recipe_data["comments"])

	for r in Recipe.objects.all():
		print((str(r))).encode('utf-8')

def add_recipe(title, views, recipeText, pictureLink, comments):
	r = Recipe.objects.get_or_create(title = title)[0]
	r.views = views
	r.recipeText = recipeText
	r.pictureLink = pictureLink
	r.save()
	for comment in comments:
		user = User.objects.get_or_create(username = "admin", password = "foodbook")
		user.save()
		c = Comment.objects.create(body = comment, user = user, recipe = r)
	return r

#Main method.
if __name__ == '__main__':
	print("Starting FoodBook population script...")
	populate()