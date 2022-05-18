from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeworkAPIView.as_view(), name='homework'),
    path('submit/', views.SubmitionAPIView().as_view(), name='submition')
]