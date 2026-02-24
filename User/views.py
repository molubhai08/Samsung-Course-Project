from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login , authenticate
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
def home(request):

    return render(request , 'index.html')

def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , password = password , username = username)

        if user:
            login(request , user)
            return redirect('landing')
        else:
            messages.error(request , "Invalid Credentials")
            return redirect('login')

    
    return render(request , 'login.html')

def register(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request , "Username Taken")
            return redirect('register')
        
        
        elif User.objects.filter(email = email).exists():
            messages.error(request , "Email Taken")
            return redirect('register')

        user = User.objects.create(
            username = username, 
            email = email
        )

        user.set_password(password)
        user.save()

        messages.info(request , "Email Taken")
        return redirect('register')


    return render(request , 'register.html')


def landing(request):
    return render(request , 'landing.html')



@login_required
def journal(request):

    if request.method == "POST":
        text = request.POST.get('j')

        Journal.objects.create(
            user = request.user,
            text = text
        )

        messages.success(request , 'Journal Submitted')
        return redirect('journal')

    return render(request , 'journal.html')
