from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login , authenticate,logout
from django.contrib import messages
from django.db.models import Q
from .models import Message

def home(request):
     if request.user.is_authenticated:
          id = request.user.id
          user = User.objects.get(id=id)
          recent_chats = Message.objects.all().filter(Q(sender_id = user)| Q(reciever_id = user))
          print(recent_chats)
          user_list = []
          for chat in recent_chats:
               if(chat.sender_id !=  user and chat.sender_id not in user_list):
                    user_list.append(chat.sender_id)
               if(chat.reciever_id != user and chat.reciever_id not in user_list):
                    user_list.append(chat.reciever_id)
          print(user_list)
          return render(request,'home.html',{'user_list':user_list})
     else:
          return render(request,'index.html')

def search_user(request):
     username = request.GET['user']
     users = User.objects.filter(username=username)
     return render(request,'search-results.html',{'users':users})


def login(request):
     if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username = username , password = password)
          if user is not None:
               auth_login(request,user)
               return redirect('/')
          else:
               messages.error(request,"Invalid Credentials")
               return redirect('/')
     
     else:
          return redirect('/')

def signup(request):
     if request.method == 'POST':
          firstname = request.POST['firstname']
          lastname = request.POST['lastname']
          username = request.POST['username']
          password = request.POST['password']
          try:
               user = User.objects.get(username=username)
               messages.error(request,"Username already exists")
               return redirect('/signup')
          except:
               user = User.objects.create_user(first_name=firstname,last_name=lastname,username=username,password=password)
               user.save()
               auth_login(request,user)
               return redirect('/')
     else:
          return render(request,'signup.html')

def Logout(request):
     logout(request)
     return redirect('/')