from django.urls import re_path , path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('<str:username>',views.user,name='user-chat')
]