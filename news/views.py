from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.core.exceptions import (ValidationError, ObjectDoesNotExist,
                                    MultipleObjectsReturned)
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from .models import Post, Vote
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
            return show_signup(request, error=valid_error)
        try:
            password = request.POST['password1']
            user = User.objects.create(username=request.POST['username'],
                                       password=password)
            validate_password(password=password, user=user)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect(current)
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


@login_required
def new_post(request):
    if request.method == 'GET':
        return render(request, 'news/new_post.html',
                      {'form': PostForm()})
    else:
        try:
            form = PostForm(request.POST)
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect(current)
        except ValueError:
            return render(request, 'news/new_post.html',
                          {'form': PostForm(), 'error': 'Bad data.'})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'GET':
        form = PostForm(instance=post)
        return render(request, 'news/edit_post.html', {'form': form,
                                                       'post': post})
    else:
        try:
            form = PostForm(request.POST, instance=post)
            form.save()
            return redirect(current)
        except ValueError:
            return render(request, 'news/edit_post.html', {'form': form,
                                                           'post': post,
                                                           'error': 'Bad Data'}
                          )


@login_required
def upvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        try:
            Vote.objects.get(user=request.user,
                             post=post)
        except ObjectDoesNotExist:
            Vote.objects.create(user=request.user, post=post)
            post.votes += 1
            post.save()
        finally:
            return redirect(current)


@login_required
def unvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        try:
            Vote.objects.delete(user=request.user, post=post)
            post.votes -= 1
            post.save()
        except ObjectDoesNotExist:
            pass
        finally:
            return redirect(current)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk, user=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect(my_posts)


def current(request):
    posts = Post.objects.all()
    ivoted = {}
    if request.user.is_authenticated:
        for post in posts:
            try:
                ivoted[post.id] = Vote.objects.get(user=request.user.id,
                                                   post=post.id)
            except ObjectDoesNotExist:
                pass
    context = {'posts': posts, 'ivoted': ivoted}
    return render(request, 'news/current.html', context)


@login_required
def my_posts(request):
    posts = Post.objects.filter(user=request.user)
    meta = {'posts': posts}
    return render(request, 'news/my_posts.html', meta)


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect(current)


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
