from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.decorators.http import require_safe, require_POST, require_http_methods

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User

# Create your views here.
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/signup.html', context)

@require_http_methods(['GET', 'POST'])
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)
        
@require_POST
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('movies:index')

@require_http_methods(['GET', 'POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)

@require_safe
def profile(request, username):
    user = get_user_model().objects.get(username=username)
    followings = user.followings.all()
    followers = user.followers.all()
    movies = user.like_movies.all()
    context = {
        'user': user,
        'followings': followings,
        'followers': followers,
        'movies': movies,
    }
    return render(request, 'accounts/profile.html', context)


def follow(request, username):
    user_to_follow = get_user_model().objects.get(username=username)
    print(user_to_follow)
    user = request.user
    print(user)
    if user != user_to_follow:
        if user_to_follow in user.followings.all():
            user.followings.remove(user_to_follow)
        else:
            user.followings.add(user_to_follow)
    return redirect('accounts:profile', user_to_follow.username)
    
