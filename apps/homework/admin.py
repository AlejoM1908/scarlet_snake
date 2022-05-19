from ast import Sub
from django.contrib import admin
from homework.models import Homework, Submition

# Use the Homework and Submition models in the django admin panel
admin.site.register(Homework)
admin.site.register(Submition)
