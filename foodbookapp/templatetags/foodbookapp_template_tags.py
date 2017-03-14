from django import template
from foodbookapp.models import Recipe

#This is for creating custom template tags.

register = template.Library()

#A template tag which gets an images thumbnail.

@register.simple_tag
def get_thumbnail(recipe):
	pictureLink = recipe.picture_link
	if pictureLink.endswith('.gif'):
		pictureLink = pictureLink[:-4]
		pictureLink = pictureLink + 'b.jpg'
	return pictureLink



