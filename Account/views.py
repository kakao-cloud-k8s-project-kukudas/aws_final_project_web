from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from Account.models import User_info, User
from django.contrib import auth
from django.contrib.auth import authenticate, login

from .forms import SignupForm
from .forms import SigninForm

# modelform을 이용한 유저 관리
def signup(request):
    signup_form=SignupForm()
    context={'forms':signup_form}
    if request.method=='GET':
        return render(request, 'account/signup.html', context)
    elif request.method=='POST':
        signup_form=SignupForm(request.POST)
        if signup_form.is_valid():
            user=User_info(
                company_name=signup_form.company_name,
                pw=signup_form.password
            )
            user.save()

            ## account user 테이블에 추가
            user = User.objects.create_user(
                username=request.POST['company_name'],
                password=request.POST['password']
            )
            auth.login(request, user)

            return redirect('/home')
        else:
            context['forms']=signup_form
            if signup_form.errors:
                for value in signup_form.errors.values():
                    context['error']=value
        return render(request, 'account/signup.html', context)    
# 로그인
def signin(request):
    signin_form=SigninForm()
    context={'forms': signin_form }
    if request.method=='GET':
        return render(request, 'account/signin.html', context)
    elif request.method=='POST':
        signin_form=SigninForm(request.POST)
        if signin_form.is_valid():
            username = request.POST['company_name']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

            # 세션 관리
            request.session['login_session']=signin_form.login_session
            request.session.set_expiry(0) # 브라우저 창 닫으면 삭제되기, 14일 보관
            return redirect('/home')
        else:
            context['forms']=signin_form
            if signin_form.errors:
                for value in signin_form.errors.values():
                    context['error']=value
        return render(request, 'account/signin.html', context)
# 로그아웃
def signout(request):
    request.session.flush()
    return redirect('/home')