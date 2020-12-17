from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your views here.


def signup_user(request):
    if request.method == 'GET':
        return render(request, 'news/signup_user.html',
                      {'form': UserCreationForm()})
    if request.method == 'POST':
        if valid_user(request.POST):
            try:
                user = User.objects.create(username=request.POST['username'],
                                           password=request.POST['password1'])
                user.save()
                return HttpResponse('Done')
            except IntegrityError as err:
                return HttpResponse(err)
        return HttpResponse('Invalid user')


def valid_user(user):
    if user['password1'] != user['password2']:
        print(user['password1'], user['password2'])
        return False
    return True
