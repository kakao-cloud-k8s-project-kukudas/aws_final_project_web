from django.contrib import admin
from django.urls import path

import Account.views

urlpatterns = [
    path("account/signup", Account.views.signup),
    path("account/signin", Account.views.signin)
]
