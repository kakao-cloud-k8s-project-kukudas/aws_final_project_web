from django.contrib import admin
from django.urls import path

import Account.views
import home.views

urlpatterns = [
    path("home", home.views.home),
    path("account/signup", Account.views.signup),
    path("account/signin", Account.views.signin),
    path("account/signout", Account.views.signout)
]
