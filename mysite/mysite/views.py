from django.shortcuts import render,redirect
from django.contrib import auth
from django.urls import reverse
from .forms import LoginForm,RegForm
from django.contrib.auth.models import User

def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request,user)
            return redirect(request.GET.get('url_from',reverse('home')))

    else:
        login_form = LoginForm()

    context = {}
    context['login_form'] = login_form
    return render(request, 'login.html', context)

def register(request):
    if request.method == 'POST':
        register_form = RegForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            new_user = User.objects.create_user(username,email,password)
            new_user.save()
            #注册成功后自动登录，返回跳转页
            user = auth.authenticate(username=username,password=password)
            auth.login(request,user)
            return redirect(request.GET.get('url_from', reverse('home')))
    else:
        register_form = RegForm()

    context = {}
    context['register_form'] = register_form
    return render(request, 'register.html', context)
