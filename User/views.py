from typing_extensions import Required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from Main.models import Message
from django.db.models import Q
from django.contrib.auth import login as auth_login , authenticate,logout
# Create your views here.

def home(request):
    return HttpResponse('home page')

def user(request,username=None):
    id = request.user.id
    user = User.objects.get(id=id)
    user0 = User.objects.get(username=username)
    messages = Message.objects.filter(Q(sender_id = user,reciever_id = user0) | Q(sender_id = user0 , reciever_id = user)).order_by('mesage_date')
     
    if request.user.is_authenticated:
        return render(request,'user-chat.html',{'user0':user0,'messages':messages})
    else:
        return render(request,'index.html')

