from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout
# Create your views here.

def signupuser(request):
    if request.method=='GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})

    else:
        #Create a new user
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(), 'error':"User name already exist"})
                

        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(), 'error':"Password did not match"})


def currenttodos(request):
    return render(request,'todo/currenttodos.html')

def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request,'todo/home.html')
