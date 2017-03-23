from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import itertools
from django.db import models

#Model for the Tag object.
class Tag(models.Model):
    title = models.CharField(max_length=20, unique = True)

    def __str__(self):
        return self.title

#Model for the Recipe object.
class Recipe(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(blank=True, unique=True)
    views = models.IntegerField(default=0)
    recipe_text = models.TextField(null = True)
    favourited_by = models.ManyToManyField(User, related_name='user_recipe_favourites',blank = True)
    favourites = models.IntegerField(default = 0)
    picture = models.ImageField(upload_to = 'recipe_images', blank = True)
    picture_link = models.URLField(blank = True)
    submitted_by = models.ForeignKey(User, null = True)
    submit_date = models.DateField(null=True)
    tags = models.ManyToManyField(Tag, related_name='recipe_tags', blank = True)
	
    #Writing our own save() to allow for extra functionality
    #in cleaning the object before saving.
    def save(self, *args, **kwargs):
        self.slug = orig = slugify(self.title)

        #Appends -1, -2, -3 to duplicate urls to ensure uniqueness.
        for x in itertools.count(1):
            if not Recipe.objects.filter(slug=self.slug).exists():
                break
            self.slug = '%s-%d' % (orig, x)

        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.title.encode('utf-8')

#Model for the UserProfile object.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slug = models.SlugField(blank= True)
    picture = models.ImageField(upload_to = 'profile_images', blank = True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
		
#Model for the Comment object.        
class Comment(models.Model):
    user = models.ForeignKey(User)
    recipe = models.ForeignKey(Recipe, related_name='on_recipe')
    body  = models.CharField(max_length=512)
    def __str__(self):
        return self.body


