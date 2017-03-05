#FoodbookApp url config. Handles all /foodbook/ urls.

from django.conf.urls import url
from foodbookapp import views


urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^new/$', views.new, name = 'new'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^recipe/(?P<recipe_slug>[\w\-]+)/$', views.show_recipe, name = 'show_recipe'),
	url(r'^register/$',views.register,name='register'),
	url(r'^add_recipe/$', views.add_recipe, name = "add_recipe"),
	url(r'^login/$', views.user_login, name='login'),
]