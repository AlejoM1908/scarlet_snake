from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.UserRegistrationAPIView.as_view(), name='register'),
    path('auth/', views.UserLoginAPIView.as_view(), name='auth'),
    path('', views.AuthUserAPIView.as_view(), name='user')
]