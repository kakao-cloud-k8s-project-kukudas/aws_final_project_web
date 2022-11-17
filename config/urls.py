from django.contrib import admin
from django.urls import path
from django.conf.urls import include


import Account.views
import home.views

urlpatterns = [
    path("home", home.views.home),
    path("account/signup", Account.views.signup),
    path("account/signin", Account.views.signin),
    path("account/signout", Account.views.signout)
]
