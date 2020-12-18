from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.core.exceptions import ValidationError
import logging
# Create your views here.

logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'news/home.html')


def signup_user(request):
    if request.method == 'GET':
        return show_signup(request)
    if request.method == 'POST':
        valid_error = valid_user(request.POST)
        if valid_error:
            return show_signup(request, valid_error)
        try:
            password = request.POST['password1']
            validate_password(password)
            user = User.objects.create(username=request.POST['username'],
                                       password=password)
            user.save()
            login(request, user)
            return redirect(current)
            return HttpResponse('DONE!')
        except IntegrityError:
            return show_signup(request, error='Username exists')
        except ValidationError as err:
            return show_signup(request, error=' '.join(err))


def login_user(request):
    if request.method == 'GET':
        return show_login(request)
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(current)
        else:
            logger.error(user)
            return show_login(request, 'Username and password do not match')


def current(request):
    meta = {}
    return render(request, 'news/current.html', meta)


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect(signup_user)


def valid_user(user):
    err = ''
    if user['password1'] != user['password2']:
        err = "Invalid new signup attempt. Passwords don't match"
    logger.info(err)
    return err


def show_signup(request, error=None):
    meta = {'form': UserCreationForm(), 'error': error}
    return render(request, 'news/signup_user.html', meta)


def show_login(request, error=None):
    meta = {'form': AuthenticationForm(), 'error': error}
    return render(request, 'news/login_user.html', meta)
