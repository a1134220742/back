from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import User, Follow
from app.serializers import appSerializer
from rest_framework import serializers
from app.zhenzismsclient import *
import random
import json
import redis
from django_redis import get_redis_connection
from django.core.cache import cache
# Create your views here.

from pymongo import MongoClient
from fake_useragent import UserAgent
import requests,json
from requests_toolbelt.multipart import MultipartEncoder

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

@api_view(['GET'])
def get_experts_by_author(request):
    client = MongoClient('10.251.252.10', 27017)
    db = client.wanfang
    collection = db.authorInfoBasic
    if request.method == 'GET':
        author = request.GET.get('author')
        experts = collection.find({'author': author})
        author_and_unit=[]
        for e in experts:
            author_and_unit.append({'author':e['author'],'unit':e['unit']})
        return JsonResponse(author_and_unit,safe=False)

@api_view(['GET'])
def get_experts_by_author_and_unit(request):
    if request.method == 'GET':
        unit = request.GET.get('unit')
        author = request.GET.get('author')
        return get_expertinfo(unit,author)

@api_view(['GET'])
def get_experts_by_author_and_id(request):
    client = MongoClient('10.251.252.10', 27017)
    db = client.wanfang
    collection = db.authorInfoBasic
    if request.method=='GET':
        id = request.GET.get('id')
        author = request.GET.get('author')
        expert=collection.find({'id':id,'author':author})[0]
        unit=expert['unit']
        return get_expertinfo(unit,author)

def get_expertinfo(unit,author):
        #总文献量
        literature_num_post = MultipartEncoder({
            'selectType': 'totalLiterature',
            'unitName': unit,
            'scholarName': author
        })
        literature_num = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/getRelevantQuota.do',
                                       data=literature_num_post,
                                       headers={'Content-Type': literature_num_post.content_type, "User-Agent": UserAgent().random})
        literature_num = json.loads(literature_num.text)
        #核心发文量
        core_num_post = MultipartEncoder({
            'selectType': 'coreNum',
            'unitName': unit,
            'scholarName': author
        })
        core_num = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/getRelevantQuota.do',
                                        data=core_num_post,
                                        headers={'Content-Type': core_num_post.content_type,
                                                 "User-Agent": UserAgent().random})
        core_num = json.loads(core_num.text)
        #总被引量
        quoted_num_post = MultipartEncoder({
            'selectType': 'sumCiteNum',
            'unitName': unit,
            'scholarName': author
        })
        quoted_num = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/getRelevantQuota.do',
                                 data=quoted_num_post,
                                 headers={'Content-Type': quoted_num_post.content_type,
                                          "User-Agent": UserAgent().random})
        quoted_num = json.loads(quoted_num.text)

        #篇均被引量
        avg_quoted_post = MultipartEncoder({
            'selectType': 'eachCiteNum',
            'unitName': unit,
            'scholarName': author
        })
        avg_quoted = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/getRelevantQuota.do',
                                       data=avg_quoted_post,
                                       headers={'Content-Type': avg_quoted_post.content_type, "User-Agent": UserAgent().random})
        avg_quoted =json.loads(avg_quoted.text)

        # 研究兴趣
        research_interest_post = MultipartEncoder({
            'number': '30',
            'unitName': unit,
            'scholarName': author
        })
        research_interest = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/researchInterest.do',
                                   data=research_interest_post,
                                   headers={'Content-Type': research_interest_post.content_type,
                                            "User-Agent": UserAgent().random})
        research_interest = json.loads(research_interest.text)

        # 发文趋势
        line_data_post = MultipartEncoder({
            'unitName': unit,
            'scholarName': author
        })
        line_data = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/lineData.do',
                                          data=line_data_post,
                                          headers={'Content-Type': line_data_post.content_type,
                                                   "User-Agent": UserAgent().random})
        line_data = json.loads(line_data.text)

        # 相关学者
        related_scholars_post = MultipartEncoder({
            'unitName': unit,
            'scholarName': author
        })
        related_scholars = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/relatedScholarsData.do',
                                  data=related_scholars_post,
                                  headers={'Content-Type': related_scholars_post.content_type,
                                           "User-Agent": UserAgent().random})
        related_scholars = json.loads(related_scholars.text)

        # 合作学者
        cooperation_scholar_post = MultipartEncoder({
            'unitName': unit,
            'scholarName': author
        })
        cooperation_scholar = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/cooperationScholarData.do',
                                         data=cooperation_scholar_post,
                                         headers={'Content-Type': cooperation_scholar_post.content_type,
                                                  "User-Agent": UserAgent().random})
        cooperation_scholar = json.loads(cooperation_scholar.text)

        return JsonResponse({'literature_num':literature_num,'core_num':core_num,'quoted_num':quoted_num,'avg_quoted':avg_quoted,\
                             'research_interest':research_interest,'line_data':line_data,'related_scholars':related_scholars,'cooperation_scholar':cooperation_scholar})

def go_follow(request):
    if request.method=='POST':
        info=json.loads(request.body)
        user_id=info['user_id']
        user_id=int(user_id)
        expert_id=info['expert_id']
        Follow.objects.create(user_id=user_id,expert_id=expert_id)
        return HttpResponse("go_follow")

def go_disfollow(request):
    if request.method=='POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        user_id = int(user_id)
        expert_id = info['expert_id']
        Follow.objects.filter(user_id=user_id,expert_id=expert_id).delete()
        return HttpResponse("go_disfollow")