import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE')

import django
django.setup()
from foodbook.models import Recipe

def populate():

