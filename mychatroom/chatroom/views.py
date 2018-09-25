import json

from dwebsocket.decorators import accept_websocket
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template.context_processors import csrf

from .models import *
from .forms import UserForm,RegisterForm
from .five import ai_answer
from .music import search_song
from .sms import send_sms

# 登录处理
def login(request):
    if request.session.get('is_login',None):
        return redirect('/chatroom/')
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            phone = login_form.cleaned_data['phone']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(phone=phone)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['phone'] = phone
                    request.session['name'] = user.name
                    return redirect('/chatroom/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())
 
    login_form = UserForm()
    return render(request, 'login.html', locals())

# 注册处理
def register(request):
    if request.session.get('is_login', None):
        return redirect("/chatroom/")
    if request.method == "POST":
        if 'code_phone' in request.POST:
            phone = request.POST['code_phone']
            request.session['verification_code'] = send_sms(phone)
            code = request.session['verification_code']
            return HttpResponse(code)
        register_form = RegisterForm()
        message = "请检查填写的内容！"
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        verification_code = request.POST['verification_code']
        email = request.POST['email']
        sex = request.POST['sex']
        same_phone_user = User.objects.filter(phone=phone)
        same_email_user = User.objects.filter(email=email)
        print(verification_code == request.session['verification_code'])
        if password != password2:  # 判断两次密码是否相同
            message = "两次输入的密码不同！"
            return render(request, 'register.html', locals())
        elif same_phone_user:  # 手机号唯一
            message = '该手机号已被注册，请登录！'
            return render(request, 'register.html', locals())
        elif same_email_user:  # 邮箱地址唯一
            message = '该邮箱地址已被注册，请使用别的邮箱！'
            return render(request, 'register.html', locals())
        elif 'verification_code' not in request.session:
            message = '请先获取验证码'
            return render(request, 'register.html', locals())
        elif verification_code != request.session['verification_code']:
            message = '验证码错误'
            return render(request, 'register.html', locals())
        # 当一切都OK的情况下，创建新用户  
        dic = {
            'phone': phone,
            'name': username,
            'password': password,
            'email': email,
            'sex': sex
        }
        User(**dic).save()
        return redirect('/chatroom/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())

# 用户消息处理
allconn = {}
@accept_websocket
def index(request):
    global allconn
    if not request.is_websocket():
        if not request.session.get('is_login',None):
            return redirect('/chatroom/login/')
        return render(request, 'chatroom.html')
    else: 
        userid = request.session['phone']
        username = request.session['name']
        userobj = User.objects.get(phone=userid)
        allconn[userid] = request.websocket
        print(userid,'connected')
        unreads = UnreadMessage.objects.filter(phone=userid)
        if unreads:
            for u in unreads:
                msg = json.dumps({'userid':u.sender.phone,
                                  'type':'new_msg',
                                  'username':u.sender.name,
                                  'msg':u.message})
                request.websocket.send(msg.encode())
            unreads.delete()
        try:
            for message in request.websocket:
                if message[:4] == b'#SS ':
                    search = message[4:].decode()
                    song_list = search_song(search)
                    msg = json.dumps({'type':'song_list','list':song_list})
                    request.websocket.send(msg.encode())
                else:
                    # 将信息发至自己的聊天框
                    msg = json.dumps({'userid':userid,
                                      'type':'new_msg',
                                      'username':username,
                                      'msg':message.decode()})
                    HistoricalMessage.objects.create(sender=userobj,message=message)
                    request.websocket.send(msg.encode())
                    # 将信息发至其他所有用户的聊天框
                    for i in allconn:
                        if i != userid:
                            allconn[i].send(msg.encode())
                    users = User.objects.exclude(phone__in=allconn)
                    for u in users:
                        UnreadMessage.objects.create(phone=u.phone,
                                                     sender=userobj,
                                                     message=message.decode())
        except Exception as e:
            print(e)
            del allconn[userid]
            print(userid,'exit')

# 用户退出
def logout(request):
    request.session.flush()
    return redirect('/chatroom/login/')

# 五子棋
def five(request):
    ai_color = request.GET.get('ai_color',None)
    if not ai_color:
        return render(request, 'five.html')
    elif ai_color == '2':
        data = request.GET.get('data',None)
        # print(data)
        i, j = ai_answer(data)
        res = {
            "sta":"succ",
            "location":[i,j]
        } 
        return HttpResponse(json.dumps(res))
    elif ai_color == 'player win':
        # data = request.GET.get('data', None)
        # res = [1,0]
        # save_train(data, res)
        return HttpResponse()
    else:
        # data = request.GET.get('data', None)
        # res = [0, 1]
        # save_train(data, res)
        return HttpResponse()
