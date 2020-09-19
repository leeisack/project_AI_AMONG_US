from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
import json

# Create your views here.
def home(request):
    return render(request, 'home.html')

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