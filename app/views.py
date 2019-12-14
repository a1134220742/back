from django.shortcuts import render

# Create your views here.
from app.models import *
import json
from rest_framework import viewsets, filters
from app.serializers import PaperSerializer
from app.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http.response import JsonResponse
from collections import Counter


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


