from django.shortcuts import render, redirect
from Signup.models import User
# Create your views here.
def base(request):
    return render(request, 'Signup/base.html')

def getPost(request): # 회원 가입 등록
    user=User()
    user.company_name=request.POST.get('company_name', None)
    user.pw=request.POST.get('pw', None)
    user.worker_min=request.POST.get('worker_min', 0)
    user.worker_max=request.POST.get('worker_max', 0)
    user.pod_min=request.POST.get('pod_min', 0)
    user.pod_max=request.POST.get('pod_max', 0)
    user.save()
    return redirect('/signup/input')



