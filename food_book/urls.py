"""food_book URL Configuration
"""
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from foodbookapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('foodbookapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
