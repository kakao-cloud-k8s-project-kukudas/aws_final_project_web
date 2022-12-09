# ssh 연결을 위해
import paramiko
from celery import shared_task
from config.celery import app
from django.shortcuts import render, redirect
from Account.models import User_info

import random
import time



# 클러스터 생성
@shared_task(bind=True)
def create_task(self, date, user):
    l = 5
    for i in range(int(l)):
        time.sleep(1)
        self.update_state(state='PROGRESS',
                              meta={'current': i, 'progress': 'installing...', 'info':'create'})
    if ssh_connect("/root/aws_final_project/terraform_script/log.sh", date, user) == 1:
        print('Task completed')
        return {'progress': 'Success!!!', 'info': 'create'}
# 클러스터 삭제
@shared_task(bind=True)
def delete_task(self, date, user):
    l = 5
    for i in range(int(l)):
        time.sleep(1)
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'progress': 'installing...', 'info':'delete'})

    if ssh_connect("/root/aws_final_project/terraform_script/terraform_destroy.sh", date, user) == 1:
        print('Destroy Success #2')
        return {'progress': 'Success!!!', 'info': 'delete'}

# ssh 연결해 동작(비동기)
def ssh_connect(command_str, args=None, args2=None):
# 로그인 세션 유지 시 SSH 접속 -> 클러스터 생성
    cli = paramiko.SSHClient()
    cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
# 호스트명이나 IP 주소 -> EC2 EndPoint 주소가 들어갈 예정
    server = "192.168.1.201"
    user = "root"
# 암호입력 숨김
    pwd = "test123"
# SSH Connect
    cli.connect(server, port=22, username=user, password=pwd)
# SSH 내의 Shell 실행
    # 인자가 있으면 인자있는걸로 실행: 클러스터 생성
    if args:
        cmd_to_execute = command_str + " " + args + " " + args2
        stdin, stdout, stderr = cli.exec_command(cmd_to_execute)
    else: # 없으면 없는 걸로 실행: 클러스터 삭제
        stdin, stdout, stderr = cli.exec_command(command_str)
    lines = stdout.readlines()
    return 1
    # for line in lines:
    #     print(line)
    #     # 클러스터 정상 생성 시 -> SSH return 1 <-- 여기부터 확인
    #     if line == '10\n':
    #         print('Apply Success #1')
    #         return 1
    #     # 클러스터 정상 삭제 시 -> SSH return 1
    #     elif line == '20\n':
    #         print('Destroy Success #1')
    #         return 1
    # cli.close()
