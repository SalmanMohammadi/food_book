from __future__ import unicode_literals
from django.contrib.auth.models import User
import uuid
from django.template.defaultfilters import slugify

from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True)
    views = models.IntegerField(default=0)
    recipe_text = models.TextField(null = True)
    favourited_by = models.ManyToManyField(User, related_name='user_recipe_favourites',blank = True)
    picture = models.ImageField(blank = True)
    picture_link = models.URLField(blank = True)
    submitted_by = models.ForeignKey(User, null = True)
    submit_date = models.DateField(null=True)
    score = models.FloatField(max_length=1, default=0)
    raters = models.IntegerField(default=0)
	
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)
    def __str__(self):
        return self.user.username

class Tag(models.Model):
    recipe = models.ForeignKey(Recipe)
    tagTitle = models.CharField(max_length=128, unique = True, default = "")
    def __str__(self):
        return self.tagTitle

class Comment(models.Model):
    commented_by = models.ForeignKey(User)
    commented_on = models.ForeignKey(Recipe)
    comment_body = models.CharField(max_length=512)
    def __str__(self):
        return self.commentBody

