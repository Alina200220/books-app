from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home-page'),
	path('register/', views.register, name='register-page'),
    path('signin/', views.sign_in, name='signin-page')
]