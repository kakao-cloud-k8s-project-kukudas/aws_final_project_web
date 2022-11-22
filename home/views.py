from django.shortcuts import render, redirect
# SSH
import paramiko

# DATE TIME
from datetime import datetime
from django.utils.dateformat import DateFormat

# Account User DB import
from Account.models import User_info

# CELERY
from .tasks import create_task, delete_task

# Create your views here.
def home(request):
    context={}
    login_session=request.session.get('login_session','')
    if login_session=='':
        context['login_session']=False
    else:
        context['login_session']=True
    return render(request, 'home/home.html', context)

# ssh connect -> 클러스터 생성
# 추가 예정 사항 : DB에 생성일자 update, 쉘 파일 실행 시 생성일자 인자로 전달하기
def create(request):
    # 생성 일자
    date = DateFormat(datetime.now()).format('mdHi')

    # ssh 연결 taks는 config/tasks.py task_func에 작성
    create_task.delay(date) # celery task 실행

    # 생성 완료 시 접속한 사용사에 해당하는 DB 생성일자 Update
    user_info_create = User_info.objects.get(company_name=request.user)
    user_info_create.date = date
    user_info_create.save()

    # 변수 선언
    context={}

    # 로그인 세션
    login_session=request.session.get('login_session','')
    if login_session=='':
        context['login_session']=False
    else:
        context['login_session']=True

    # 클러스터 두번 생성 원인, render로 했을경우 새로고침 시 /home/create가 다시 불러와짐 
    return redirect('/home')

# ssh connect -> 클러스터 삭제
def delete(request):
    # 사용사에 해당하는 DB 생성일자 가져오기
    user_info_delete = User_info.objects.get(company_name=request.user)
    delete_date = user_info_delete.date

    # ssh 연결 taks는 config/tasks.py task_func에 작성
    delete_task.delay(delete_date) # celery task 실행

    return redirect('/home')
