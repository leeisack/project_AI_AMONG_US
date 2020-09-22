from django.shortcuts import render, redirect
from .models import User
from .models import UserAccount
from .models import UserNotice
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import time
import smtplib, os
from email import encoders #이미지 같은것을 문자열로 변환해줌
from email.mime.text import MIMEText #메세지의 제목을 설정하기 위한 모듈
from email.mime.multipart import MIMEMultipart #메세지의 내용을 설정하기 위한 모듈
from email.mime.base import MIMEBase #전송할 때 사용하는 모듈

# Create your views here.

ERROR_MSG = {
    'ID_EXIST': '이미 사용 중인 아이디 입니다.',
    'ID_NOT_EXIST': '존재하지 않는 아이디 입니다.',
    'ID_PW_MISSING': '아이디와 비밀번호를 확인해주세요.',
    'PW_CHECK': '비밀번호가 일치하지 않습니다.'
}

def manual(request) :
    return render(request, 'manual.html')

def home(request) :
    notice = UserNotice.objects.all()
    context = {'notice': notice}
    return render(request, 'home.html', context)

@csrf_exempt
def id_check(request):
    json_dict = json.loads(request.body)
    id_check = User.objects.filter(username = json_dict['id']).exists()
    test = {'error': id_check}
    return JsonResponse(test)

def signup(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        }
    }

    if request.method == "POST":

        user_id = request.POST['id']
        user_pw = request.POST['pwd']
        user_pw_check = request.POST['pwd_chk']

        # 추가
        user_name = request.POST['name']
        user_phone_num = request.POST['phone']
        user_email = request.POST['email']

        if (user_id and user_pw):

            user = User.objects.filter(username=user_id)

            if len(user) == 0:

                if user_pw == user_pw_check:

                    created_user = User.objects.create_user(
                        username=user_id,
                        password=user_pw
                    )

                    # 추가
                    UserAccount.objects.create(
                        user=created_user,
                        name=user_name,
                        phone_num=user_phone_num,
                        email=user_email
                    )

                    auth.login(request, created_user)

                    return redirect('home')

                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_EXIST']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'signup.html', context)

def login(request):
    context = {
        'error': {
            'state': False,
            'msg': ''
        },
    }

    if request.method == 'POST':
        user_id = request.POST['id']
        user_pw = request.POST['pwd']

        user = User.objects.filter(username=user_id)

        if (user_id and user_pw):
            if len(user) != 0:

                user = auth.authenticate(
                    username=user_id,
                    password=user_pw
                )

                if user != None:
                    auth.login(request, user)

                    return redirect('home')
                else:
                    context['error']['state'] = True
                    context['error']['msg'] = ERROR_MSG['PW_CHECK']
            else:
                context['error']['state'] = True
                context['error']['msg'] = ERROR_MSG['ID_NOT_EXIST']

        else:
            context['error']['state'] = True
            context['error']['msg'] = ERROR_MSG['ID_PW_MISSING']

    return render(request, 'login.html', context)

@csrf_exempt
def notice(request):
    error = False
    json_dict = json.loads(request.body)
    UserNotice.objects.create(
        current_user = request.user,
        current_time = json_dict['time'],
        current_notice = '비정상적인 접근'
    )
    error = True
    test = {'error': error}
    return JsonResponse(test)

def logout(request):
    
    auth.logout(request)

    return redirect('manual')

@csrf_exempt
def email(request):

    account = UserAccount.objects.all()
    for i in account :
        if i.user == request.user :
            user_email = i.email
    # img = ImageGrab.grab()
    # saveas = 'screenshot.png'
    # img.save(saveas)
    # 발송 이메일
    fromaddress = 'sackda24@likelion.org'
    pw = 'aiamongus'

    #수신 이메일
    toaddress = user_email

    #이메일 제목
    msg = MIMEMultipart()
    msg['Subject'] = '비정상적인 움직임이 포착됐습니다.'

    #이메일 내용
    text = MIMEText('비정상적인 움직임이 있습니다. 확인부탁드립니다.https://imhelloworld.tk')

    #이메일 제목과 내용 합치기
    msg.attach(text)

    s = smtplib.SMTP('smtp.gmail.com',587) #587: google smpt server password
    s.starttls() #tls방식으로 smpt 서버 접속
    s.login(fromaddress, pw) #fromaddress에 로그인

    # #이미지첨부
    # image = r'C:\Users\sackd\Desktop\images.png'
    # # image = image.encode('utf-8')


    # part = MIMEBase("application","octet-stream")
    # part.set_payload(open(image,'rb').read())
    # encoders.encode_base64(part)
    # part.add_header("content-Disposition","attachment",filename='image.png')
    # msg.attach(part)

    s.sendmail(fromaddress,toaddress,msg.as_string())
    s.quit()