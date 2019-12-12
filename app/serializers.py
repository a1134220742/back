from app.models import *
from rest_framework import serializers

class PaperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wanfangpro
        fields =('id','c_abstract','c_author','c_keywords','c_periodical','c_title','e_periodical','e_title','fund','indexid','time','units','url')