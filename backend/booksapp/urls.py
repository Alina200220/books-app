from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    path('home/', user_views.book_search, name='home-page'),
	path('', user_views.register, name='register-page'),
    path('profile/', user_views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('add-book/', user_views.add_book, name='add_book'),
]
    
