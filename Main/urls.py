# from django.conf import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('search',views.search_user,name='search-user'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name="signup"),
    path('logout',views.Logout,name='logout'),
]