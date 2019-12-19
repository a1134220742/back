from app.models import *
from rest_framework import serializers

class PaperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wanfangpro
        fields =('id','c_abstract','c_author','c_keywords','c_periodical','c_title','e_periodical','e_title','fund','indexid','time','units','url')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields =('id','name','pwd','balance','phone_num')


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favorite
        fields =('id','user_id','paper_id')


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChatList
        fields =('sender_name','receiver_name','content')

