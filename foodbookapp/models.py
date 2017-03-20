from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from django.db import models

class Tag(models.Model):
    tagTitle = models.CharField(max_length=128, unique = True, default = "")
    def __str__(self):
        return self.tagTitle

class Recipe(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True, unique=True)
    views = models.IntegerField(default=0)
    recipe_text = models.TextField(null = True)
    favourited_by = models.ManyToManyField(User, related_name='user_recipe_favourites',blank = True)
    favourites = models.IntegerField(default = 0)
    picture = models.ImageField(blank = True)
    picture_link = models.URLField(blank = True)
    submitted_by = models.ForeignKey(User, null = True)
    submit_date = models.DateField(null=True)
    tags = models.ManyToManyField(Tag, related_name='recipe_tags', blank = True)
	
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(blank = True)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    com_user = models.ForeignKey(User)
    com_recipe = models.ForeignKey(Recipe, related_name='onRecipe')
    com_body  = models.CharField(max_length=512)
    def __str__(self):
        return self.com_body
