from django.contrib import admin
from django.urls import path

import Signup.views

urlpatterns = [
    path("signup/input", Signup.views.base),
    path("signup/getPost", Signup.views.getPost),
     # path("signin/", include('signin.urls'))
]
