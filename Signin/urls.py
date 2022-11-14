# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views

# user>views에서 모든 함수를 가져온다.
from .views import *

app_name = "signin"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='signin/login.html'), name='login'),
]

