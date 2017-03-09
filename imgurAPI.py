from imgurpython import ImgurClient
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_book.settings')

import django
django.setup()
from foodbookapp.models import Recipe

def get_images():
	client_id = 'a07481456742e43'
	client_secret = '2046f8fb4c75f5bba6d0312a1519957571ffd88e'

	client = ImgurClient(client_id, client_secret)

	# Example request
	items = client.subreddit_gallery(subreddit = "GifRecipes")
	recipes = {}
	for item in items:
		curRecipe = {}
		curRecipe["title"] = item.title
		curRecipe["views"] = item.views
		curRecipe["pictureLink"] = item.link
		recipes[item.title] = curRecipe

	for r, recipe_data in recipes.items():
		add_recipe(recipe_data["title"],recipe_data["views"], "",  recipe_data["pictureLink"])

	for r in Recipe.objects.all():
		print((str(r)))

def add_recipe(title, views, recipeText, pictureLink):
	r = Recipe.objects.get_or_create(title = title)[0]
	r.views = views
	r.recipeText = recipeText
	r.pictureLink = pictureLink
	r.save()
	return r

if __name__ == '__main__':
	print("Starting..")
	get_images()