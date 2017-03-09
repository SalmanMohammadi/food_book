from __future__ import unicode_literals
from django.contrib.auth.models import User
import uuid
from django.template.defaultfilters import slugify

from django.db import models

class Recipe(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True)
    views = models.IntegerField(default=0)
    recipeText = models.TextField(blank = True)
    favouritedBy = models.ManyToManyField(User, related_name='user_recipe_favourites',blank = True)
    picture = models.ImageField(blank = True)
    pictureLink = models.URLField(blank = True)
    submittedBy = models.ForeignKey(User,null = True)
    submitDate = models.forms.DateField(null=True)
	
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    userID = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)
    def __str__(self):
        return self.user.username

class Tag(models.Model):
    recipe = models.ForeignKey(Recipe)
    tagTitle = models.CharField(max_length=128, unique = True, default = "")
    def __str__(self):
        return self.tagTitle

class Comment(models.Model):
    commentedBy = models.ForeignKey(User)
    commentedOn = models.ForeignKey(Recipe)
    commentBody = models.CharField(max_length=512)
    def __str__(self):
        return self.commentBody

