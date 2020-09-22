from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import requests
import smtplib, os
from email import encoders #이미지 같은것을 문자열로 변환해줌
from email.mime.text import MIMEText #메세지의 제목을 설정하기 위한 모듈
from email.mime.multipart import MIMEMultipart #메세지의 내용을 설정하기 위한 모듈
from email.mime.base import MIMEBase #전송할 때 사용하는 모듈
from PIL import ImageGrab
# Create your views here.
def home(request):
    return render(request, 'home.html')

def manual(request):
    return render(request, 'manual.html')

def signup(request):
    # if request.method == 'POST':
    #     user_id = request.POST['id']
    #     user_pw = request.POST['pwd']
    return render(request, 'signup.html')

@csrf_exempt
def id_check(request):
    json_dict = json.loads(request.body)

    id_check = User.objects.filter(username = json_dict['id']).exists()

    test = {'error': id_check}

    return JsonResponse(test)

def login(request):
    return render(request, 'login.html')

def kakao(request):
    # 커스텀 템플릿 주소 : https://kapi.kakao.com/v2/api/talk/memo/send
    talk_url = "https://kapi.kakao.com/v2/api/talk/memo/send"

    # 사용자 토큰
    token = '098b3361420f6ad3b6c17afd67800814'
    header = {
        "Authorization": "Bearer pTultU4OZNt--y0GXGg0fGURVvhJ1Ogd3-UmpgopyV8AAAF0s6v-0w".format(
            token=token
        )
    }

    # 메시지 template id와 정의했던 ${name}을 JSON 형식으로 값으로 입력
    payload = {
        'template_id' : '36836'
    }

    # 카카오톡 메시지 전송
    res = requests.post(talk_url, data=payload, headers=header)

    if res.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
        return render(request)
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(res.json()))
        return render(request)

def email(request):
    # img = ImageGrab.grab()
    # saveas = 'screenshot.png'
    # img.save(saveas)
    # 발송 이메일
    fromaddress = 'sackda24@likelion.org'
    pw = '96952425'

    #수신 이메일
    toaddress = 'sackda24@naver.com'

    #이메일 제목
    msg = MIMEMultipart()
    msg['Subject'] = '비정상적인 움직임이 포착됐습니다.'

    #이메일 내용
    text = MIMEText('비정상적인 움직임이 있습니다. 확인부탁드립니다.')

    #이메일 제목과 내용 합치기
    msg.attach(text)

    s = smtplib.SMTP('smtp.gmail.com',587) #587: google smpt server password
    s.starttls() #tls방식으로 smpt 서버 접속
    s.login(fromaddress, pw) #fromaddress에 로그인

    #이미지첨부
    image = r'C:\Users\sackd\Desktop\images.png'
    # image = image.encode('utf-8')


    part = MIMEBase("application","octet-stream")
    part.set_payload(open(image,'rb').read())
    encoders.encode_base64(part)
    part.add_header("content-Disposition","attachment",filename='image.png')
    msg.attach(part)

    s.sendmail(fromaddress,toaddress,msg.as_string())
    s.quit()