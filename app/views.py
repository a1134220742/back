from django.shortcuts import render

# Create your views here.
from app.models import *
import json
from rest_framework import viewsets, filters
from app.serializers import PaperSerializer
from app.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def paperList(request):
    if request.method=='GET':
        keyword = request.GET.get('keyword')
        page = int(request.GET.get('page'))
        queryset = Wanfangpro.objects.filter(c_title__contains=keyword)[(page-1)*10:page*10]
        serializer = PaperSerializer(queryset,many=True)
        return Response(serializer.data)

# class PapersViewSet(viewsets.ModelViewSet):
#     queryset = Wanfangpro.objects.filter(c_title__contains='机器')
#     serializer_class = PaperSerializer(queryset, many=True)
