from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from Account.models import User_info, User
from django.contrib import auth
from django.contrib.auth import authenticate, login

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


from .forms import SignupForm
from .forms import SigninForm

# modelform을 이용한 유저 관리
def signup(request):
    signup_form=SignupForm()
    context={'forms':signup_form}
    if request.method=='GET':
        return render(request, 'account/signup_bs.html', context)
    elif request.method=='POST':
        signup_form=SignupForm(request.POST)
        if signup_form.is_valid():
            username = request.POST.get('company_name')
            company_initial = request.POST.get('company_initial')
            password = request.POST.get('password')

            try:
                User.objects.get(username=username)
                messages.error(request, '이미 존재하는 아이디입니다.')
                return redirect('/account/signup')
            except ObjectDoesNotExist:
                User.objects.create_user(username=username, password=password)
                user_info = User_info(company_name=username, company_initial=company_initial)
                user_info.save()
                messages.success(request, '회원가입에 성공하였습니다.')
                return redirect('/account/signin')
        else:
            context['forms']=signup_form
            if signup_form.errors:
                for value in signup_form.errors.values():
                    context['error']=value
        return render(request, 'account/signup_bs.html', context)    
# 로그인
def signin(request):
    signin_form=SigninForm()
    context={'forms': signin_form }
    if request.method=='GET':
        return render(request, 'account/signin_bs.html', context)
    elif request.method=='POST':
        signin_form=SigninForm(request.POST)
        if signin_form.is_valid():
            username = request.POST.get('company_name')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            # 인증된 사용자경우
            if user is not None:
                login(request, user)
                request.session['login_session'] = signin_form.login_session
                request.session.set_expiry(0)  # 브라우저 창 닫으면 삭제되기, 14일 보관
                return redirect('/home')
            else:
                messages.error(request, 'ID 혹은 비밀번호 오류입니다.')
                return redirect('/account/signin')
        else:
            context['forms']=signin_form
            if signin_form.errors:
                for value in signin_form.errors.values():
                    context['error']=value
        return render(request, 'account/signin_bs.html', context)
# 로그아웃
def signout(request):
    request.session.flush()
    return redirect('/home')