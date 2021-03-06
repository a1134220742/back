import pymongo
import gridfs
from bson import ObjectId
from pymongo import MongoClient
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.models import User, Follow
# from app.serializers import appSerializer
from rest_framework import serializers
from app.zhenzismsclient import *
import random
import json
import redis
from django_redis import get_redis_connection
from django.core.cache import cache
from django.core import serializers
# Create your views here.

from pymongo import MongoClient
from fake_useragent import UserAgent
import requests, json
from requests_toolbelt.multipart import MultipartEncoder

# Create your views here.
from app.models import *
import json
from rest_framework import viewsets, filters
from app.serializers import PaperSerializer
from app.serializers import UserSerializer
from app.serializers import FavoriteSerializer
from app.serializers import ChatSerializer
from app.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from collections import Counter
from elasticsearch import Elasticsearch

import pymongo as pm

client = pm.MongoClient('10.251.252.10', 27017)
db = client['wanfang']
collection = db['authorInfoBasic']


@api_view(['POST'])
def login(request):
    postBody = request.body
    print(request.POST)
    result = json.loads(postBody)
    user = User.objects.filter(name=result['username'])
    if (user.count() == 0):
        result = {"code": "-2", "isexpert": "-1"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    if (user[0].pwd == result['password']):
        # request.session['username'] = result['username']
        if user[0].expert_id == None:
            result = {"code": "0", "isexpert": "-1", "username": user[0].name}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
        else:
            result = {"code": "0", "isexpert": "0", "username": user[0].name}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")
    else:
        result = {"code": "-1", "isexpert": "-1"}
        return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json")


@api_view(['POST'])
def message(request):
    postBody = request.body
    result = json.loads(postBody)
    code = ''
    for num in range(1, 5):
        code = code + str(random.randint(0, 9))
    tel = result['phone']

    # Redis
    cache.set(tel, code)

    client = ZhenziSmsClient('https://sms_developer.zhenzikj.com', '102458', 'f9ab7d85-bea0-48ef-875b-6895f4838061');
    params = {'message': '您的验证码为:' + code, 'number': result['phone']};
    send_result = client.send(params);
    send_result = json.loads(send_result)
    if (send_result["code"] == 0):
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
        user = User.objects.create(name=result['username'], pwd=result['password'], balance=0.00,
                                   phone_num=result['phone'])
        user.save()
    return HttpResponse(0)


@api_view(['POST'])
def verify(request):
    postBody = request.body
    result = json.loads(postBody)
    code = cache.get(result['phone'])
    if (result['code'] == code):
        return HttpResponse(0)
    else:
        return HttpResponse(-1)


@api_view(['POST'])
def islogin(request):
    postBody = request.body
    result = json.loads(postBody)
    user = User.objects.filter(name=result['username'])
    if user.count() > 0:
        info = {"login": "1"}
        info2 = serializers.serialize("json", user)
        info["userinfo"] = json.loads(info2)
        return HttpResponse(json.dumps(info), content_type="application/json")
    else:
        info = {"login": "-1", "userinfo": "null"}
        return HttpResponse(json.dumps(info), content_type="application/json")


@api_view(['GET'])
def paperInfo(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        es = Elasticsearch([{'host': '10.251.252.10', 'port': 9200}])
        re = es.search(
            body={
                'query': {
                    'multi_match': {
                        'query': keyword,
                        'fields': ['c_title', 'c_keywords', 'c_abstract']

                    }
                }
            }
        )
        li = []
        au = []
        for res in re['hits']['hits']:
            str = res['_source']["time"][0:4]
            if str not in li:
                li.append(str)
            au = au + res['_source']["c_author"].split(',')
        li.sort()
        au_p = Counter(au).most_common(5)
        au.clear()
        for e in au_p:
            au.append(e[0])
        data = {
            'total': re["hits"]["total"]["value"],
            'authors': au,
            'years': li,
        }
        return JsonResponse(data)


@api_view(['GET'])
def paperGet(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        page = int(request.GET.get('page'))
        es = Elasticsearch([{'host': '10.251.252.10', 'port': 9200}])
        re = es.search(
            body={
                'query': {
                    'multi_match': {
                        'query': keyword,
                        'fields': ['c_title', 'c_keywords', 'c_abstract']

                    }
                },
                "from": (page - 1) * 10
            }
        )
        li = []
        for res in re['hits']['hits']:
            del res['_source']['@timestamp']
            del res['_source']['type']
            del res['_source']['@version']
            li.append(res['_source'])
        # queryset1 = Wanfangpro.objects.filter(c_title__contains=keyword)
        # queryset2 = Wanfangpro.objects.filter(c_keywords__contains=keyword)
        # queryset3 = Wanfangpro.objects.filter(c_abstract__contains=keyword)
        # queryset = (queryset1|queryset2|queryset3).distinct()[(page-1)*10:page*10]
        # serializer = PaperSerializer(queryset,many=True)
        return Response(li)


@api_view(['GET'])
def paperGetByYear(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        page = int(request.GET.get('page'))
        year = request.GET.get('year')
        es = Elasticsearch([{'host': '10.251.252.10', 'port': 9200}])
        re = es.search(
            body={
                'query': {
                    'bool': {
                        'must': [
                            {
                                'multi_match': {
                                    'query': keyword,
                                    'fields': ['c_title', 'c_keywords', 'c_abstract']

                                }
                            },
                            {
                                "match_phrase": {
                                    "time": year
                                }
                            }

                        ]
                    }
                },
                "from": (page - 1) * 10
            }
        )
        li = []
        for res in re['hits']['hits']:
            del res['_source']['@timestamp']
            del res['_source']['type']
            del res['_source']['@version']
            li.append(res['_source'])
        return Response(li)


@api_view(['GET'])
def paperGetByAuthor(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        page = int(request.GET.get('page'))
        author = request.GET.get('author')
        es = Elasticsearch([{'host': '10.251.252.10', 'port': 9200}])
        re = es.search(
            body={
                'query': {
                    'bool': {
                        'must': [
                            {
                                'multi_match': {
                                    'query': keyword,
                                    'fields': ['c_title', 'c_keywords', 'c_abstract']

                                }
                            },
                            {
                                "match_phrase": {
                                    "c_author": author
                                }
                            }

                        ]
                    }
                },
                "from": (page - 1) * 10
            }
        )
        li = []
        for res in re['hits']['hits']:
            del res['_source']['@timestamp']
            del res['_source']['type']
            del res['_source']['@version']
            li.append(res['_source'])
        return Response(li)


@api_view(['GET'])
def paperGetByYearTotal(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        year = request.GET.get('year')
        es = Elasticsearch([{'host': '10.251.252.10', 'port': 9200}])
        re = es.search(
            body={
                'query': {
                    'bool': {
                        'must': [
                            {
                                'multi_match': {
                                    'query': keyword,
                                    'fields': ['c_title', 'c_keywords', 'c_abstract']

                                }
                            },
                            {
                                "match_phrase": {
                                    "time": year
                                }
                            }

                        ]
                    }
                }
            }
        )
        data = {
            'total': re["hits"]["total"]["value"]
        }
        return JsonResponse(data)


@api_view(['GET'])
def paperGetByAuthorTotal(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        author = request.GET.get('author')
        es = Elasticsearch([{'host': '10.251.252.10', 'port': 9200}])
        re = es.search(
            body={
                'query': {
                    'bool': {
                        'must': [
                            {
                                'multi_match': {
                                    'query': keyword,
                                    'fields': ['c_title', 'c_keywords', 'c_abstract']

                                }
                            },
                            {
                                "match_phrase": {
                                    "c_author": author
                                }
                            }

                        ]
                    }
                }
            }
        )
        data = {
            'total': re["hits"]["total"]["value"]
        }
        return JsonResponse(data)


@api_view(['GET'])
def paperGetID(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        queryset = Wanfangpro.objects.filter(id=id)
        serializer = PaperSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_favorites(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        queryset0 = User.objects.filter(name=name)
        user_id = queryset0[0].id
        queryset1 = Favorite.objects.filter(user_id=user_id)

        if queryset1.count() == 0:
            return Response([])

        queryset3 = Wanfangpro.objects.filter(id=queryset1[0].id)
        for a in queryset1:
            queryset2 = Wanfangpro.objects.filter(id=a.paper_id)
            queryset3 = queryset3 | queryset2

        serializer = PaperSerializer(queryset3, many=True)
        return Response(serializer.data)
    # chatlist = ChatList.objects.create(sender_name=result['sender'], receiver_name=result['receiver'], content=result['content'])
    # chatlist.save()


@api_view(['GET'])
def get_user_by_name(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        queryset1 = User.objects.filter(name=name)
        if queryset1[0].expert_id:
            data = {
                "userType": "expert",
                "phoneNumber": queryset1[0].phone_num,
                "money": str(queryset1[0].balance)
            }
        else:
            data = {
                "userType": "user",
                "phoneNumber": queryset1[0].phone_num,
                "money": str(queryset1[0].balance)
            }
        return JsonResponse(data)


@api_view(['GET'])
def get_follows(request):
    if request.method == 'GET':
        username = request.GET.get('name')
        queryset0 = User.objects.filter(name=username)
        user_id = queryset0[0].id
        queryset1 = Follow.objects.filter(user_id=user_id)
        # print(json.dumps(list(queryset1),ensure_ascii=False))
        #
        if queryset1.count() == 0:
             return Response([])

        result = []
        for a in queryset1:
            oneexpert = collection.find({"_id": ObjectId(a.expert_id)})
            for e in oneexpert:
                data = {
                    "name": e['author'],
                    "location": e['unit'],
                    "avatar": '',
                    "isFollowed": True
                }
                result.append(data)
        return Response(result)


@api_view(['GET'])
def get_chat_list(request):
    if request.method == 'GET':
        username = request.GET.get('name')
        queryset0 = ChatList.objects.filter(sender_name=username)
        queryset1 = ChatList.objects.filter(receiver_name=username)
        queryset2 = queryset0 | queryset1

        if queryset2.count() == 0:
            return Response([])

        chats = []
        for a in queryset2:
            item = {
                "date": a.date,
                "sender": a.sender_name,
                "receiver": a.receiver_name,
                "content": a.content
            }
            chats.append(item)

        set_mark1 = {i['sender'] for i in chats}
        set_mark2 = {i['receiver'] for i in chats}
        set_mark1.update(set_mark2)
        records = []
        for mark in set_mark1:  # 分组
            if mark == username:
                continue
            one = [dict_current for dict_current in chats if
                   dict_current['sender'] == mark or dict_current['receiver'] == mark]
            records.append(one)

        results = []
        for a in records:
            a.sort(key=lambda stu: stu["date"])
            if a[0]['sender'] == username:
                oneresult = {
                    "name": a[0]['receiver'],
                    "record": a
                }
            else:
                oneresult = {
                    "name": a[0]['sender'],
                    "record": a
                }
            results.append(oneresult)

        return JsonResponse(results, safe=False)


@api_view(['POST'])
def post_message(request):
    post_body = request.body
    result = json.loads(post_body)

    chatlist = ChatList.objects.create(sender_name=result['sender'], receiver_name=result['receiver'],
                                       content=result['content'])
    chatlist.save()

    if chatlist:
        result = {
            "success": True
        }
    else:
        result = {
            "success": False
        }
    return JsonResponse(result)


@api_view(['GET'])
def get_experts_by_author(request):
    client = MongoClient('10.251.252.10', 27017)
    db = client.wanfang
    collection = db.authorInfoBasic
    if request.method == 'GET':
        author = request.GET.get('author')
        experts = collection.find({'author': author})
        author_and_unit = []
        for e in experts:
            author_and_unit.append({'author': e['author'], 'unit': e['unit']})
        return JsonResponse(author_and_unit, safe=False)


@api_view(['GET'])
def get_experts_by_author_and_unit(request):
    if request.method == 'GET':
        unit = request.GET.get('unit')
        author = request.GET.get('author')
        return get_expertinfo(unit, author)


@api_view(['GET'])
def get_experts_by_author_and_id(request):
    client = MongoClient('10.251.252.10', 27017)
    db = client.wanfang
    collection = db.authorInfoBasic
    if request.method == 'GET':
        id = request.GET.get('id')
        author = request.GET.get('author')
        re = collection.find({'id': id, 'author': author})
        re = list(re)
        print(re)
        if len(re) > 0:
            expert = re[0]
            unit = expert['unit']
            data = {
                "unit": unit
            }
            return JsonResponse(data, safe=False)
        else:
            data = {
                "unit": ''
            }
            return JsonResponse(data, safe=False)


def get_expertinfo(unit, author):
    # 总文献量
    literature_num_post = MultipartEncoder({
        'selectType': 'totalLiterature',
        'unitName': unit,
        'scholarName': author
    })
    literature_num = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/getRelevantQuota.do',
                                   data=literature_num_post,
                                   headers={'Content-Type': literature_num_post.content_type,
                                            "User-Agent": UserAgent().random})
    literature_num = json.loads(literature_num.text)
    # 核心发文量
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
    # 总被引量
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

    # 篇均被引量
    avg_quoted_post = MultipartEncoder({
        'selectType': 'eachCiteNum',
        'unitName': unit,
        'scholarName': author
    })
    avg_quoted = requests.post('http://miner.wanfangdata.com.cn/scholarsBootPage/getRelevantQuota.do',
                               data=avg_quoted_post,
                               headers={'Content-Type': avg_quoted_post.content_type, "User-Agent": UserAgent().random})
    avg_quoted = json.loads(avg_quoted.text)

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

    return JsonResponse(
        {'literature_num': literature_num, 'core_num': core_num, 'quoted_num': quoted_num, 'avg_quoted': avg_quoted, \
         'research_interest': research_interest, 'line_data': line_data, 'related_scholars': related_scholars,
         'cooperation_scholar': cooperation_scholar})


def go_follow(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        user_id = int(user_id)
        expert_id = info['expert_id']
        Follow.objects.create(user_id=user_id, expert_id=expert_id)
        return HttpResponse("go_follow")


@api_view(['GET'])
def add_favorites(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        queryset0 = User.objects.filter(name=name)
        user_id = queryset0[0].id
        paper_id = request.GET.get('id')
        Favorite.objects.create(user_id=user_id, paper_id=paper_id)


@api_view(['GET'])
def remove_favorites(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        queryset0 = User.objects.filter(name=name)
        user_id = queryset0[0].id
        paper_id = request.GET.get('id')
        Favorite.objects.filter(user_id=user_id, paper_id=paper_id).delete()
        return HttpResponse("remove_favorites")


def go_disfollow(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        user_id = int(user_id)
        expert_id = info['expert_id']
        Follow.objects.filter(user_id=user_id, expert_id=expert_id).delete()
        return HttpResponse("go_disfollow")


def go_follow_by_user_id_and_author_and_unit(request):
    client = MongoClient('10.251.252.10', 27017)
    db = client.wanfang
    collection = db.authorInfoBasic
    if request.method == 'POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        author = info['author']
        unit = info['unit']
        experts = collection.find({'author': author, 'unit': unit})
        expert_id = 0
        for e in experts:
            expert_id = e['_id']
        if expert_id == 0:
            collection.insert_one({'id': '000000000000000000000000', 'author': author, 'unit': unit})
            expert_id = '000000000000000000000000'
        Follow.objects.create(user_id=user_id, expert_id=expert_id)
        return HttpResponse("go_follow_by_user_id_and_author_and_unit")


def go_disfollow_by_user_id_and_author_and_unit(request):
    client = MongoClient('10.251.252.10', 27017)
    db = client.wanfang
    collection = db.authorInfoBasic
    if request.method == 'POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        author = info['author']
        unit = info['unit']
        experts = collection.find({'author': author, 'unit': unit})
        for e in experts:
            expert_id = e['_id']
        Follow.objects.filter(user_id=user_id, expert_id=expert_id).delete()
        return HttpResponse("go_disfollow_by_user_id_and_author_and_unit")


def get_head_url(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        imageurl = info['imageurl']
        User.objects.filter(id=user_id).update(head_url=imageurl)
        return HttpResponse("get_head_url")


def application_for_expert(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        user_id = info['user_id']
        real_name = info['real_name']
        ID_number = info['ID_number']
        institution = info['institution']
        credentials_url = info['credentials_url']
        expert_name = info['author']
        expert_unit = info['unit']
        temp = Applicationforexpert.objects.latest('id')
        Applicationforexpert.objects.create(id=temp.id + 1, user_id=user_id, real_name=real_name, id_number=ID_number,
                                            institution=institution, credentials_url=credentials_url,
                                            expert_name=expert_name, expert_unit=expert_unit)
        return HttpResponse("application_for_expert")


def handle_the_application(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        application_id = info['application_id']
        opt = info['opt']
        if opt == '0':
            Applicationforexpert.objects.filter(id=application_id).delete()
        elif opt == '1':
            client = MongoClient('10.251.252.10', 27017)
            db = client.wanfang
            collection = db.authorInfoBasic
            application = Applicationforexpert.objects.filter(id=application_id)[0]
            experts = collection.find({'author': application.expert_name, 'unit': application.expert_unit})
            for e in experts:
                expert_id = e['id']
            User.objects.filter(id=application.user_id).update(expert_id=expert_id)
            Applicationforexpert.objects.filter(id=application_id).delete()
        return HttpResponse("handle_the_application")


@api_view(['GET'])
def get_iffollowed(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        author = request.GET.get('author')
        unit = request.GET.get('unit')
        client = MongoClient('10.251.252.10', 27017)
        db = client.wanfang
        collection = db.authorInfoBasic
        experts = collection.find({'author': author, 'unit': unit})
        for e in experts:
            expert_id = e['id']
        iffollowed = Follow.objects.filter(user_id=user_id, expert_id=expert_id)
        ret = '0' if len(iffollowed) == 0 else '1'
        return JsonResponse({'iffollowed': ret})


def newest(request):
    articles = Wanfangpro.objects.filter(id__contains='5de')[0:9]
    ret = []
    for article in articles:
        ret.append({'id': article.id, 'title': article.c_title, 'url': article.url})
    return JsonResponse(ret, safe=False)


def admin_login(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        username = info['username']
        password = info['password']
        administrator = Administrator.objects.filter(name=username)[0]
        ret = 0 if administrator.password == password else -1
        return HttpResponse(ret)


def admin_getData(request):
    if request.method == 'GET':
        all = Applicationforexpert.objects.filter()
        ret = []
        for application in all:
            ret.append({'id': application.id, 'user_id': application.user_id, 'real_name': application.real_name,
                        'ID_number': application.id_number, 'institution': application.institution,
                        'credentials_url': application.credentials_url, 'expert_name': application.expert_name,
                        'expert_unit': application.expert_unit})
        return JsonResponse(ret, safe=False)


def get_id_by_name(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        username = info['username']
        user = User.objects.filter(name=username)
        data = {
            "id": user[0].id
        }
        return JsonResponse(data, safe=False)
