from django.urls import path

from custom_auth.views import LoginView, RegisterView, logout_user


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterView.as_view(), name='register')
]
