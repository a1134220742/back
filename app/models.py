# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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

