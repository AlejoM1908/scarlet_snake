from django.contrib import admin
from course.models import Course

# Use the Course model in the django admin panel
admin.site.register(Course)
