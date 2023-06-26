from django.urls import path

from .views import index, login, logout, register

app_name = "accounts"

urlpatterns = [

    path('', index),
    path('problem', index),
    path('forgot-password', index),
    path("login", login),
    path("logout", logout),
    path("register", register),

]
