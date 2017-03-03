from django.contrib import admin
from foodbookapp.models import UserProfile, Recipe

# Register your models here.
# class RecipeAdmin(admin.ModelAdmin):
# 	list_display = ('title',)

admin.site.register(Recipe)
admin.site.register(UserProfile)