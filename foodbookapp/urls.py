#FoodbookApp url config. Handles all /foodbook/ urls.

from django.conf.urls import url
from foodbookapp import views

urlpatterns = [
	url(r'^$', views.home, name = 'home'),
	url(r'^home/(?P<page_name>[\w]+)?$', views.home, name = 'home'),
	url(r'^favourited/$', views.favourited, name='favourited'),
	url(r'^about/$', views.about, name = 'about'),
	url(r'^recipe/(?P<recipe_slug>[\w\-]+)/$', views.show_recipe, name = 'show_recipe'),
	url(r'^register/$',views.register,name='register'),
	url(r'^add_recipe/$', views.add_recipe, name = 'add_recipe'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^profile/$', views.user_profile, name='profile'),
	url(r'^favourite/(?P<type>[\w]+)$', views.fav_recipe, name = 'favourite'),
	url(r'^recipe/(?P<recipe_slug>[\w\-]+)/comment/$', views.add_comment, name = 'add_comment'),
	url(r'^recipe/(?P<recipe_slug>[\w\-]+)/tag/$', views.add_tag, name = 'add_tag'),
	url(r'^search/$', views.search, name = 'search'),
	url(r'^tagsearch/$',views.tag_search,name='tag_search')]