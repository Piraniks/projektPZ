import json

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from custom_auth.forms import RegisterForm, LoginForm
from custom_auth.models import User


class RegisterView(View):
    TEMPLATE = 'auth/register.html'
    USER_EXISTS_ALREADY_MESSAGE = 'User with given username exists already.'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.TEMPLATE)

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "errors": json.loads(form.errors.as_json())
            }
            return render(request, self.TEMPLATE, context=context)

        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            User.objects.create_user(username, password)
        except IntegrityError:
            context = {
                "errors": {
                    "username": [{
                        "message": self.USER_EXISTS_ALREADY_MESSAGE
                    }],
                }
            }
            return render(request, self.TEMPLATE, context=context)

        return redirect('login')


class LoginView(View):
    TEMPLATE = 'auth/login.html'
    USER_DOES_NOT_EXIST_MESSAGE = 'No user exists with given credentials.'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.TEMPLATE)

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            context = {
                "errors": json.loads(form.errors.as_json())
            }
            return render(request, self.TEMPLATE, context=context)

        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            context = {
                "errors": {
                    "user": [{
                        "message": self.USER_DOES_NOT_EXIST_MESSAGE
                    }],
                }
            }
            return render(request, self.TEMPLATE, context=context)

        login(request, user)
        return redirect('device_list')


def logout_user(request):
    logout(request)
    return redirect('index')
