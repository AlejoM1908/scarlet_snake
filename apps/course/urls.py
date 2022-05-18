from django.urls import path
from . import views

urlpatterns = [
    path('', views.CourseAPIView.as_view(), name='course')
]