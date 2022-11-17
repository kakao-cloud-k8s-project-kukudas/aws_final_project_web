from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from Account.models import User

from .forms import SignupForm

# modelform을 이용한 유저 관리
def signup(request):
    signup_form=SignupForm()
    context={'forms':signup_form}
    if request.method=='GET':
        return render(request, 'Signup/signup.html', context)
    elif request.method=='POST':
        signup_form=SignupForm(request.POST)
        if signup_form.is_valid():
            user=User(
                company_name=signup_form.company_name,
                pw=signup_form.password
            )
            user.save()
            return redirect('/account/')
        else:
            context['forms']=signup_form
            if signup_form.errors:
                for value in signup_form.errors.values():
                    context['error']=value
        return render(request, 'Signup/signup.html', context)
     

        
# 로그인


# 로그아웃