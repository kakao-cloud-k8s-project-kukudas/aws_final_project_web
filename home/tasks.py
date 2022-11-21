# ssh 연결을 위해
import paramiko
from celery import shared_task

# 클러스터 생성
@shared_task(bind=True)
def create_task(self):
    date="2022"
#     stdin, stdout, stderr = cli.exec_command("/root/aws_final_project/terraform/terraform_made.sh", date)
    ssh_connect("/root/test_juyeon/test.sh", date)

# 클러스터 삭제
@shared_task(bind=True)
def delete_task(self):
    # "cd /root/aws_final_project/terraform/11181923 && terraform destroy -auto-approve && rm -rf ../11181923"
    ssh_connect("/root/test_juyeon/test.sh")

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
        stdin, stdout, stderr = cli.exec_command(command_str, args)
    else: # 없으면 없는 걸로 실행: 클러스터 삭제
        stdin, stdout, stderr = cli.exec_command(command_str)
    lines = stdout.readlines()
    print(''.join(lines))
    cli.close()