from django import forms

from custom_auth.validators import (
    username_regex_validator, username_length_validator,
    password_length_validator)


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=64,
        validators=[username_regex_validator, username_length_validator]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        validators=[password_length_validator]
    )
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError('Passwords does not match.')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
