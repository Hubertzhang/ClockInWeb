# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from django.contrib import auth
from moge_web.admin import UserCreationForm
from moge_web.models import *


# Create your views here.


def index(request):
    if not request.user.is_authenticated():
        return render(request, "login.html")
    current_lists = List.objects.order_by('-time')
    if len(current_lists) == 0:
        return render(request, "index.html")
    current_list = current_lists[0]
    is_in = request.user in current_list.persons.all()
    if request.method == 'POST':
        if is_in:
            current_list.persons.remove(request.user)
        else:
            current_list.persons.add(request.user)
        return HttpResponseRedirect('/')
    if request.user in current_list.persons.all():
        return render(request, "index.html", {'activity': current_list.title,
                                              'join': True})
    return render(request, "index.html", {'activity': current_list.title,
                                          'join': False})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def login(request, error_msg=""):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return render(request, "login.html", {'error': "该用户已经被禁止登陆",
                                                      'username': username})
        else:
            return render(request, "login.html", {'error': "用户名或密码不正确",
                                                  'username': username})
    else:
        return render(request, "login.html", context=error_msg or {})


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid() and request.POST['password1'] and len(request.POST['password1']) >= 6:
            form.save()
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            username = request.POST['username'] if request.POST['username'] else ""
            password1 = request.POST['password1'] if request.POST['password1'] else ""
            password2 = request.POST['password2'] if request.POST['password2'] else ""
            name = request.POST['name'] if request.POST['name'] else ""
            email = request.POST['email'] if request.POST['email'] else ""
            error_msg = "错误"
            if not username:
                error_msg = "请输入用户名"
            elif not (password1 and password2):
                error_msg = "请输入密码"
            elif not name:
                error_msg = "请输入昵称"
            elif not email:
                error_msg = "请输入邮箱"
            elif password1 != password2:
                error_msg = "两次密码不一致"
            elif len(password1) < 6:
                error_msg = "密码长度小于6位"
            elif User.objects.filter(username=username):
                error_msg = "用户名已经存在"
                username = ""
            elif User.objects.filter(email=email):
                error_msg = "邮箱已经注册"
                email = ""
            elif User.objects.filter(name=name):
                error_msg = "昵称已经被使用"
                name = ""
            return render(request, "register.html", {'error': error_msg,
                                                     'username': username,
                                                     'name': name,
                                                     'email': email})
    return render(request, "register.html")


@require_http_methods(["GET"])
def display(request, list_id=-1):
    if list_id == -1:
        lists = List.objects.all()
        res = []
        for x in lists:
            res.append({'id': x.id, 'title': x.title})
        return render(request, "display.html", {'title': "活动列表",
                                                 'num': len(res),
                                                 'list': res})
    mlist = List.objects.get(id=list_id)
    if not mlist:
        return HttpResponseRedirect('/display')
    res = []
    for x in mlist.persons.all():
        res.append(x.name)
    return render(request, "display.html", {'title': mlist.title + "参加人员",
                                             'num': len(res),
                                             'list': res})
