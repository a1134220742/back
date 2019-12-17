from django.shortcuts import render

# Create your views here.
from app.models import *
import json
from rest_framework import viewsets, filters
from app.serializers import PaperSerializer
from app.serializers import UserSerializer
from app.serializers import FavoriteSerializer
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
        if queryset1[0].expertID :
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
            oneexpert = User.objects.filter(id = a.expert_id)
            head_url = oneexpert[0].head_url

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
def get_followst(request):
    if request.method=='GET':

        oneexpert = collection.find_one({ "id": "5de33f240031bb949dbd684d" },{'_id':0})
        print(oneexpert.get('id'))
        a = json.dumps(oneexpert, ensure_ascii=False)
        print(a)
        b = json.loads(a)
        print(b)

        return JsonResponse({})

