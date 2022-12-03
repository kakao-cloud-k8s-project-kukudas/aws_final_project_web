from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from home.views import task_status, run_long_task

import Account.views
import home.views

urlpatterns = [
    path("home", home.views.home),
    path("account/signup", Account.views.signup),
    path("account/signin", Account.views.signin),
    path("account/signout", Account.views.signout),
    path('run-long-task/', run_long_task, name='run_long_task'),
    path('task-status/<str:task_id>/', task_status, name='task_status'),
]
