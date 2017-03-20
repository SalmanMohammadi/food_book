from imgurpython import ImgurClient
import os
from datetime import datetime
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_book.settings')

import django
django.setup()
from foodbookapp.models import Recipe

def get_images():
	client_id = 'a07481456742e43'
	client_secret = '2046f8fb4c75f5bba6d0312a1519957571ffd88e'

	client = ImgurClient(client_id, client_secret)

	items = client.subreddit_gallery(subreddit = "GifRecipes",sort = "top", window = "all")
	recipes = {}
	for item in items:
		curRecipe = {}
		if not Recipe.objects.filter(title = item.title).exists():
			curRecipe["title"] = item.title
			curRecipe["views"] = item.views

			pictureLink = item.link[:-4]
			if(pictureLink.endswith("h") and len(pictureLink) == 27):
				pictureLink = pictureLink[:-1]
			pictureLink = pictureLink + ".gif"  

			curRecipe["picture_link"] = pictureLink
			curRecipe["submit_date"] = time.strftime('%Y-%m-%d', time.localtime(item.datetime))
			print item.title
			print(curRecipe["submit_date"])
			recipes[item.title] = curRecipe

	for r, recipe_data in recipes.items():
		add_recipe(recipe_data["title"],recipe_data["views"], None,  recipe_data["picture_link"], recipe_data["submit_date"])

def add_recipe(title, views, recipeText, picture_link, submit_date):
	r = Recipe.objects.get_or_create(title = title)[0]
	r.views = views
	r.recipeText = recipeText
	r.picture_link = picture_link
	r.submit_date = submit_date
	r.favourites = 0
	r.save()
	return r

if __name__ == '__main__':
	print("Starting..")
	get_images()