from datetime import timezone
from django.forms.utils import to_current_timezone
from django.http.response import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
# Create your views here.


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})

    else:
        # Create a new user
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': "User name already exist"})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': "Password did not match"})


def currenttodos(request):
    todos = Todo.objects.filter(user = request.user,datecompleted__isnull = True)
    return render(request, 'todo/currenttodos.html',{'todos':todos})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def home(request):
    return render(request, 'todo/home.html')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})

    else:
        # Login user
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user:
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), "error": "User do not exist"})


def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:

            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),'error':'Some Error occured'})


def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
    if request.method=='GET':

        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html',{'todo':todo,'form':form})
    else:
        try:

            form = TodoForm(request.POST,instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html',{'todo':todo,'form':form,'error':'bad info'})

def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
    if request.method=='POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk, user = request.user)
    if request.method=='POST':
        todo.delete()
        return redirect('currenttodos')