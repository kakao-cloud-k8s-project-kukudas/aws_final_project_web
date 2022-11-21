from django.shortcuts import render, redirect
# SSH
import paramiko

# DATE TIME
from datetime import datetime
from django.utils.dateformat import DateFormat

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
    # ssh 연결 taks는 config/tasks.py task_func에 작성
    create_task.delay() # celery task 실행
# 변수 선언
    context={}

# 로그인 세션
    login_session=request.session.get('login_session','')
    if login_session=='':
        context['login_session']=False
    else:
        context['login_session']=True

# 생성일자
    date = DateFormat(datetime.now()).format('Ymd')

# DB update : 생성일자 추가

    # 클러스터 두번 생성 원인, render로 했을경우 새로고침 시 /home/create가 다시 불러와짐 
    return redirect('/home')

# ssh connect -> 클러스터 삭제 ** 미완성 **
def delete(request):
    # ssh 연결 taks는 config/tasks.py task_func에 작성
    delete_task.delay() # celery task 실행
# 변수 선언
    context={}
    login_session=request.session.get('login_session','')

# 생성하는 Date
    date = DateFormat(datetime.now()).format('Ymd')
    
    return redirect('/home')
