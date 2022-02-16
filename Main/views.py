from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login , authenticate,logout
from django.contrib import messages


def home(request):
     if request.user.is_authenticated:
          return render(request,'home.html')
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