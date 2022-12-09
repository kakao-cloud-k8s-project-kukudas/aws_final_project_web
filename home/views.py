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
from django.http import JsonResponse
from celery.result import AsyncResult



def home(request):
    context={}
    login_session=request.session.get('login_session','')
    if login_session=='':
        context['login_session']=False
    else:
        context['login_session']=True
    # 클러스터가 이미 있는 경우 DB 주소 주기

    return render(request, 'home/home_bs.html', context)

# ssh connect -> 클러스터 생성
# 추가 예정 사항 : DB에 생성일자 update, 쉘 파일 실행 시 생성일자 인자로 전달하기
def run_long_task(request):
    if request.method == 'POST':
        if request.POST.get('l') == "1":
            # Create 인 경우
            print('POST')
            # DB 조회
            user_info_create = User_info.objects.get(company_name=request.user)
            # 생성 일자
            date = DateFormat(datetime.now()).format('Hi')
            # 클러스터 이름 설정
            cluster_name = user_info_create.company_initial + date
            # ssh 연결 taks는 config/tasks.py task_func에 작성
            if user_info_create.cluster_exist == 0:
                user_info_create.date = date
                user = user_info_create.company_name
                user_info_create.save()
                task = create_task.delay(cluster_name, user)  # celery task 실행

                return JsonResponse({"task_id": task.id}, status=202)
            else:
                print("클러스터가 생성 중이거나 이미 생성됨")
        # 클러스터 삭제..task
        elif request.POST.get('l') == "2":
            print('DELETE')
            # 사용사에 해당하는 DB 생성일자 가져오기
            user_info_delete = User_info.objects.get(company_name=request.user)
            cluster_name = user_info_delete.company_initial + user_info_delete.date
            user = user_info_delete.company_name

            if user_info_delete.cluster_exist == 1:
                task_delete = delete_task.delay(cluster_name, user)

                return JsonResponse({"task_id": task_delete.id}, status=202)
            else:
                print("삭제 할 클러스터가 없습니다.")  # <-- 앞단에서 설명 창이 있음 좋겠음

def task_status(request, task_id):
    task = AsyncResult(task_id)
    if task.state == 'FAILURE' or task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'progression': "PENDING",
            'info': str(task.info)
        }
        return JsonResponse(response, status=200)
    progression = task.info.get('progress')
    info = task.info.get('info')
    response = {
        'task_id': task_id,
        'state': task.state,
        'progression': progression,
        'info': info
    }
    return JsonResponse(response, status=200)

def url_moodle(request):
    print("GO MOODLE")
    if request.user.is_authenticated:
        moodle_addr = "http://" + User_info.objects.get(company_name=request.user).lb_address
        print(moodle_addr)

        return redirect(moodle_addr)

def url_grafana(request):
    print("GO GRAFANA")
    if request.user.is_authenticated:
        grafana_addr = "http://" + User_info.objects.get(company_name=request.user).grafana_address
        print(grafana_addr)
        return redirect(grafana_addr)