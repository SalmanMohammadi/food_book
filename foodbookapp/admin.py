from django.contrib import admin
from foodbookapp.models import UserProfile, Recipe, Tag, Comment

# Register your models here.
# class RecipeAdmin(admin.ModelAdmin):
# 	list_display = ('title',)

admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Comment)