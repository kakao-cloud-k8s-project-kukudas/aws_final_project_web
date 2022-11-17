from django.contrib import admin
from django.urls import path

import Account.views
urlpatterns = [
    path("account/", Account.views.signup),
]
