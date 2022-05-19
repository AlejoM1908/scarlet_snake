from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User

# Use the User model in the django admin panel
admin.site.register(User, UserAdmin)
