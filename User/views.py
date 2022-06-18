from typing_extensions import Required
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from Main.models import Message
from django.db.models import Q
from django.core import serializers
from json import dumps
import json
from django.contrib.auth import login as auth_login , authenticate,logout
# Create your views here.

def home(request):
    return HttpResponse('home page')

def user(request,username=None):
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(id=id)
        user0 = User.objects.get(username=username)
        recent_chats = Message.objects.all().filter(Q(sender_id = user)| Q(reciever_id = user))
        user_list = []
        for chat in recent_chats:
            if(chat.sender_id !=  user and chat.sender_id not in user_list):
                user_list.append(chat.sender_id)
            if(chat.reciever_id != user and chat.reciever_id not in user_list):
                user_list.append(chat.reciever_id)
            
        messages = Message.objects.filter(Q(sender_id = user,reciever_id = user0) | Q(sender_id = user0 , reciever_id = user)).order_by('mesage_date')    
        read_messages = messages.filter(sender_id = user0)
        for i in read_messages:
            i.read = True
            i.save()
            print(i.read)
        x = serializers.serialize('json',messages)
        # print(x)
        
        return render(request,'user-chat.html',{'user0':user0,'datajson':x,'user_list':user_list,'messages':messages})
    else:
        return render(request,'index.html')

