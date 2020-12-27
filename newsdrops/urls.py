"""newsdrops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from news import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # auth
    path('signup/', views.signup_user, name='signup_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    # current
    path('', views.current, name='current'),
    path('add/', views.new_post, name='new_post'),
    path('my/', views.my_posts, name='my_posts'),
    path('post/<int:pk>', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete', views.delete_post, name='delete_post'),
    path('post/<int:pk>/upvote', views.upvote_post, name='upvote_post'),

]
