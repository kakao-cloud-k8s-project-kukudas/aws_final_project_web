from django.contrib import admin
from django.urls import path
from django.conf.urls import include


import Signup.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("signup/input", Signup.views.base),
    path("signup/getPost", Signup.views.getPost),
    path('signin/', include('Signin.urls')),
]
