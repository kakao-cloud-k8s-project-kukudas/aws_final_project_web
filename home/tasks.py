# ssh 연결을 위해
import paramiko
from celery import shared_task

from django.shortcuts import redirect
from Account.models import User_info


# 클러스터 생성
@shared_task(bind=True)
def create_task(self, date, user):
    if ssh_connect("/root/aws_final_project/terraform/terraform_made.sh", date) == 1:
        print('Apply Success #2')
        user_info_create = User_info.objects.get(company_name=user)
        user_info_create.cluster_exist = 1
        user_info_create.save()
        print('Apply Success #3')

        return True

# 클러스터 삭제
@shared_task(bind=True)
def delete_task(self, date, user):
    if ssh_connect("/root/aws_final_project/terraform/terraform_destroy.sh", date) == 1:
        print('Destroy Success #2')
        user_info_delete = User_info.objects.get(company_name=user)
        user_info_delete.cluster_exist = 0
        user_info_delete.save()
        print('Destroy Success #3')
        return True

# ssh 연결해 동작(비동기)
def ssh_connect(command_str, args=None):
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
        cmd_to_execute = command_str + " " + args
        stdin, stdout, stderr = cli.exec_command(cmd_to_execute)
    else: # 없으면 없는 걸로 실행: 클러스터 삭제
        stdin, stdout, stderr = cli.exec_command(command_str)

    for line in lines:
        print(line)
        # 클러스터 정상 생성 시
        if line == '10\n':
            print('Apply Success #1')
            return 1
        # 클러스터 정상 삭제 시
        elif line == '20\n':
            print('Destroy Success #1')
            return 1
    cli.close()