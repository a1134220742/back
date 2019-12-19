from django.shortcuts import render

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

import pymongo as pm
client=pm.MongoClient('10.251.252.10',27017)
db=client['wanfang']
collection=db['authorInfoBasic']


@api_view(['GET'])
def paperInfo(request):
    if request.method=='GET':
        keyword = request.GET.get('keyword')
        queryset1 = Wanfangpro.objects.filter(c_title__contains=keyword)
        queryset2 = Wanfangpro.objects.filter(c_keywords__contains=keyword)
        queryset3 = Wanfangpro.objects.filter(c_abstract__contains=keyword)
        queryset = (queryset1|queryset2|queryset3).distinct()
        li = []
        au = []
        for e in queryset:
            str = e.time[0:4]
            if str not in li:
                li.append(str)
            au = au + e.c_author.split(',')
        li.sort()
        au_p = Counter(au).most_common(5)
        au.clear()
        for e in au_p:
            au.append(e[0])
        data = {
            'total':queryset.count(),
            'authors':au,
            'years':li,
        }
        return JsonResponse(data)


@api_view(['GET'])
def paperGet(request):
    if request.method=='GET':
        keyword = request.GET.get('keyword')
        page = int(request.GET.get('page'))
        queryset1 = Wanfangpro.objects.filter(c_title__contains=keyword)
        queryset2 = Wanfangpro.objects.filter(c_keywords__contains=keyword)
        queryset3 = Wanfangpro.objects.filter(c_abstract__contains=keyword)
        queryset = (queryset1|queryset2|queryset3).distinct()[(page-1)*10:page*10]
        serializer = PaperSerializer(queryset,many=True)
        return Response(serializer.data)


@api_view(['GET'])
def paperGetID(request):
    if request.method=='GET':
        id = request.GET.get('id')
        queryset = Wanfangpro.objects.filter(id = id)
        serializer = PaperSerializer(queryset,many=True)
        return Response(serializer.data)


@api_view(['GET'])
def get_favorites(request):
    if request.method=='GET':
        name = request.GET.get('name')
        queryset0 = User.objects.filter(name = name)
        user_id = queryset0[0].id
        queryset1 = Favorite.objects.filter(user_id = user_id)
        queryset3 = Wanfangpro.objects.filter(id = queryset1[0].id)
        for a in queryset1:
            queryset2 = Wanfangpro.objects.filter(id = a.paper_id)
            queryset3 = queryset3 | queryset2

        serializer = PaperSerializer(queryset3,many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_user_by_name(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        queryset1 = User.objects.filter(name = name)
        if queryset1[0].expert_id :
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
    if request.method=='GET':
        username = request.GET.get('name')
        queryset0 = User.objects.filter(name = username)
        user_id = queryset0[0].id
        queryset1 = Follow.objects.filter(user_id = user_id)
        result = []
        for a in queryset1:
            oneexpert = User.objects.filter(expert_id = a.expert_id)
            if len(oneexpert):
                head_url = oneexpert[0].head_url
            else:
                head_url = None

            oneexpert = collection.find_one({ "id": a.expert_id },{'_id':0})

            data = {
                "name": oneexpert.get('author'),
                "location": oneexpert.get('unit'),
                "avatar": head_url,
                "isFollowed": True
            }
            result.append(data)

        # json_result = json.dumps(result, ensure_ascii=False)
        return JsonResponse(result, safe=False)


@api_view(['GET'])
def get_chat_list(request):
    if request.method=='GET':
        username = request.GET.get('name')
        queryset0 = ChatList.objects.filter(sender_name=username)
        queryset1 = ChatList.objects.filter(receiver_name=username)
        queryset2 = queryset0 | queryset1
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
            one = [dict_current for dict_current in chats if dict_current['sender'] == mark or dict_current['receiver'] == mark]
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

    chatlist = ChatList.objects.create(sender_name=result['sender'], receiver_name=result['receiver'], content=result['content'])
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


