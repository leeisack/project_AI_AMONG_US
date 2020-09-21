from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json
import requests

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
        "Authorization": "Bearer GgYQtrbNg1VxdTRt30NqdSDZoUWE7GNgyhNKBAopb1UAAAF0ry7VrQ".format(
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
    