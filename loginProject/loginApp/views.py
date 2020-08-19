from django.shortcuts import redirect, render
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    return render(request, 'index.html')


def success(request):
    context = {}
    if 'user_id' not in request.session:
        return redirect('/')
        context = {
            'user': User.objects.get(id=request.session[user_id])
        }

    return render(request, 'success.html', context)



def register(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        hash_browns = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = hash_browns,
        )     
        request.session['user_id'] = user.id
        return redirect('/success')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_to_login = User.objects.get(email=request.POST['login_email'])
        request.session['user_id'] = user_to_login.id 
        return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')



