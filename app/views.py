from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import User
from app.serializers import appSerializer
from rest_framework import serializers
from app.zhenzismsclient import *
import random
import json
import redis
from django_redis import get_redis_connection
from django.core.cache import cache
# Create your views here.

@api_view(['POST'])
def login(request):
    postBody = request.body
    print(request.POST)
    result = json.loads(postBody)
    user = User.objects.get(name=result['username'])
    if(user.pwd == result['password']):
        request.session['username'] = result['username']
        return HttpResponse(0)
    else:
        return HttpResponse(-1)


@api_view(['POST'])
def message(request):
    postBody = request.body
    result = json.loads(postBody)
    code = ''
    for num in range(1,5):
        code = code + str(random.randint(0,9))
    tel = result['phone']

    # Redis
    cache.set(tel,code)

    client = ZhenziSmsClient('https://sms_developer.zhenzikj.com','102458', 'f9ab7d85-bea0-48ef-875b-6895f4838061');
    params = {'message': '您的验证码为:'+code, 'number': result['phone']};
    send_result = client.send(params);
    if(send_result != None):
        return HttpResponse(0)
    else:
        return HttpResponse(-1)

@api_view(['POST'])
def register(request):
    postBody = request.body
    result = json.loads(postBody)
    user = User.objects.filter(name=result['username'])
    if user:
        return HttpResponse(-1)
    else:
        user = User.objects.create(name=result['username'], pwd=result['password'], balance=0.00,phone_num=result['phone'])
        user.save()
    return HttpResponse(0)

@api_view(['POST'])
def verify(request):
    postBody = request.body
    result = json.loads(postBody)
    code = cache.get(result['phone'])
    if(result['code'] == code):
        return HttpResponse(0)
    else:
        return HttpResponse(-1)