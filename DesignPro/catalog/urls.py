from django.urls import path
from .views import index, profile, UserLoginView
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', index, name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
]