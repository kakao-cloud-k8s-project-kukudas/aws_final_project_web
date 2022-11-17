from django.shortcuts import render

# Create your views here.
def home(request):
    context={}
    login_session=request.session.get('login_session','')
    if login_session=='':
        context['login_session']=False
    else:
        context['login_session']=True
    return render(request, 'home/home.html', context)