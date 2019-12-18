from django.db import models

# Create your models here.
from django.db import models

class Wanfangpro(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    c_abstract = models.TextField(blank=True, null=True)
    c_author = models.TextField(blank=True, null=True)
    c_keywords = models.TextField(blank=True, null=True)
    c_periodical = models.TextField(blank=True, null=True)
    c_title = models.TextField(blank=True, null=True)
    e_periodical = models.TextField(blank=True, null=True)
    e_title = models.TextField(blank=True, null=True)
    fund = models.TextField(blank=True, null=True)
    indexid = models.TextField(db_column='indexID', blank=True, null=True)  # Field name made lowercase.
    time = models.TextField(blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wanfangPro'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    name = models.TextField(blank=True, null=True)
    pwd = models.TextField(blank=True, null=True)
    balance = models.TextField(blank=True, null=True)
    phone_num = models.TextField(blank=True, null=True)
    expertID = models.TextField(blank=True, null=True)
    head_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Favorite(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    user_id = models.TextField(blank=False, null=False)
    paper_id = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'favorite'


class Follow(models.Model):
    id = models.CharField(primary_key=True, max_length=24)
    user_id = models.TextField(blank=False, null=False)
    expert_id = models.TextField(blank=False, null=False)

    class Meta:
        managed = False
        db_table = 'follow'


class Chat(models.Model):
    sender_name = models.TextField(blank=False, null=False)
    receiver_name = models.TextField(blank=False, null=False)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_list'

