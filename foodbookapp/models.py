from __future__ import unicode_literals
from django.contrib.auth.models import User
import uuid

from django.db import models

class Recipe(models.Model):
    recipeID = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=128)
    slug = models.URLField(unique=True)
    views = models.IntegerField(default=0)
    recipeText = models.TextField()
    favouritedBy = models.ForeignKey(User)
    submittedBy = models.ForeignKey(User, unique = True)
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
    tagTitle = models.CharField(max_length=128)
    def __str__(self):
        return self.tagTitle

class Comment(models.Model):
    commentedBy = models.ForeignKey(User)
    commentedOn = models.ForeignKey(Recipe)
    commentBody = models.CharField(max_length=512)
    def __str__(self):
        return self.commentBody

