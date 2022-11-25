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
    # 변수 선언
    context={}
    # DB 조회
    user_info_create = User_info.objects.get(company_name=request.user)
    # 생성 일자
    date = DateFormat(datetime.now()).format('Hi')
    # 클러스터 이름 설정
    cluster_name = user_info_create.company_initial + '_' + date
    # ssh 연결 taks는 config/tasks.py task_func에 작성
    if user_info_create.cluster_exist == 0:
        user_info_create.date = date
        user = user_info_create.company_name
        user_info_create.save()
        create_task.delay(cluster_name, user) # celery task 실행
    else:
        print("클러스터가 생성 중이거나 이미 생성됨") # <-- 앞단에서 설명 창이 있음 좋겠음

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
    cluster_name = user_info_delete.company_initial + '_' + user_info_delete.date
    user = user_info_delete.company_name

    if user_info_delete.cluster_exist == 1:
        delete_task.delay(cluster_name, user)
    else:
        print("삭제 할 클러스터가 없습니다.") # <-- 앞단에서 설명 창이 있음 좋겠음
    return redirect('/home')
