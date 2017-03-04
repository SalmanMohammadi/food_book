#FoodbookApp url config. Handles all /foodbook/ urls.

from django.conf.urls import url
from foodbookapp import views

urlpatterns = [
	url(r'^$', views.new, name = 'new'),
	url(r'^new/$', views.new, name = 'new'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^recipe/(?P<recipe_slug>[\w\-]+)/$', views.show_recipe, name = 'show_recipe'),
]