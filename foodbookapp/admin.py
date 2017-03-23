from django.contrib import admin
from foodbookapp.models import UserProfile, Recipe, Tag, Comment

#Registers models for editing and viewing in the admin interface.

admin.site.register(Recipe)
admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Comment)