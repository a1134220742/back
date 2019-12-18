from rest_framework import serializers
from app.models import *
class appSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id','name','pwd','balance','phone_num')