from django.shortcuts import render
# SSH
import paramiko

# DATE TIME
from datetime import datetime
from django.utils.dateformat import DateFormat

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
def create(request):
# 변수 선언
    context={}
#     login_session=request.session.get('login_session','')

# 생성하는 Date
    date = DateFormat(datetime.now()).format('Ymd')

# login session 확인
#     if login_session=='':
#         context['login_session']=False
#     else:
#         context['login_session']=True

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
    stdin, stdout, stderr = cli.exec_command("/root/aws_final_project/terraform/terraform_made.sh")
    lines = stdout.readlines()
    print(''.join(lines))
    cli.close()

    return render(request, 'home/home.html', context)

# ssh connect -> 클러스터 삭제
def delete(request):
# 변수 선언
    context={}
    login_session=request.session.get('login_session','')

# 생성하는 Date
    date = DateFormat(datetime.now()).format('Ymd')

# login session 확인
    if login_session=='':
        context['login_session']=False
    else:
        context['login_session']=True

# 로그인 세션 유지 시 SSH 접속 -> 클러스터 생성
        cli = paramiko.SSHClient()
        cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)
# 호스트명이나 IP 주소
        server = "192.168.1.201"
        user = "root"
# 암호입력 숨김
        pwd = "test123"
# SSH Connect
        cli.connect(server, port=22, username=user, password=pwd)
# SSH 내의 Shell 실행
        stdin, stdout, stderr = cli.exec_command("cd /root/aws_final_project/terraform/11181923 && terraform destroy -auto-approve && rm -rf ../11181923")
        lines = stdout.readlines()
        print(''.join(lines))
        cli.close()

    return render(request, 'home/home.html', context)
