"""classroom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title= 'Classroom API',
        default_version= 'v1',
        description= 'API for classroom functionalities',
        terms_of_service= 'https://www.google.com/policies/terms/',
        contact= openapi.Contact(email= 'contact@snipplets.local'),
        license= openapi.License(name= 'BSD License')
    ),
    public= True,
    permission_classes= (permissions.AllowAny),
    authentication_classes= ()
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Internal API URL's
    path('user/', include('apps.user.urls')),
    path('homework/', include('apps.homework.urls')),
    path('course/', include('apps.course.urls')),
    # API swager documentation URL's
    path(
        'swager.json', 
        schema_view.with_ui('swager', cache_timeout= 0), 
        name= 'schema-json'
    ),
    path(
        'swager/', 
        schema_view.with_ui('swager', cache_timeout= 0), 
        name= 'schema-swager-ui'
    ),
    path(
        'redoc/', 
        schema_view.with_ui('redoc', cache_timeout= 0), 
        name= 'schema-redoc'
    ),
]
