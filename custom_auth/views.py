import json

from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from custom_auth.forms import RegisterForm, LoginForm
from custom_auth.models import User


class RegisterView(View):
    TEMPLATE_PATH = 'auth/register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.TEMPLATE_PATH)

    def post(self, request):
        form = RegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "errors": json.loads(form.errors.as_json())
            }
            return render(request, self.TEMPLATE_PATH, context=context)

        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            User.objects.create_user(username, password)
        except IntegrityError:
            context = {
                "errors": {
                    "username": [{
                        "message": "User with given username exists already."
                    }],
                }
            }
            return render(request, self.TEMPLATE_PATH, context=context)

        return redirect('login')


class LoginView(View):
    TEMPLATE_PATH = 'auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, self.TEMPLATE_PATH)

    def post(self, request):
        form = LoginForm(request.POST)

        if not form.is_valid():
            context = {
                "errors": json.loads(form.errors.as_json())
            }
            return render(request, self.TEMPLATE_PATH, context=context)

        cleaned_data = form.cleaned_data
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            context = {
                "errors": {
                    "user": [{
                        "message": "No user exists with given credentials."
                    }],
                }
            }
            return render(request, self.TEMPLATE_PATH, context=context)

        login(request, user)
        return redirect('index')


def logout_user(request):
    logout(request)
    return redirect('index')
