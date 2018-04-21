from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction, IntegrityError

from custom_auth.forms import RegisterForm, LoginForm
from custom_auth.models import User


class RegisterView(View):
    REGISTER_TEMPLATE_PATH = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.REGISTER_TEMPLATE_PATH)

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            errors = form.errors
            return render(request, self.REGISTER_TEMPLATE_PATH, context={'errors': errors})

        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        new_user = User(username=username)
        new_user.set_password(password)

        # Save as an atomic operation
        try:
            with transaction.atomic():
                new_user.save()
        except IntegrityError:
            context = {
                'error_messages': ['User with given username exists.']
            }
            return render(request, self.REGISTER_TEMPLATE_PATH, context=context)

        return redirect('index')


class LoginView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'auth/login.html')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if not form.is_valid():
            errors = form.errors
            return render(request, 'auth/login.html', context={'errors': errors})

        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            context = {
                'error_messages': ['No user exists with given credentials.']
            }
            return render(request, 'auth/login.html', context=context)

        login(request, user)
        return redirect('index')


def logout_user(request, *args, **kwargs):
    logout(request)
    return redirect('index')
