#FoodbookApp url config. Handles all /foodbook/ urls.

from django.conf.urls import url
from foodbookapp import views

urlpatterns = [
	url(r'^$', views.index, name = 'index'),
	url(r'^new/$', views.new, name = 'new'),
]