from django.db import models

# Create your models here.
from django.db import models


class Favorite(models.Model):
    user_id = models.IntegerField()
    paper_id = models.CharField(max_length=24)

    class Meta:
        managed = False
        db_table = 'favorite'


class Follow(models.Model):
    user_id = models.IntegerField()
    expert_id = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'follow'


class User(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    phone_num = models.CharField(max_length=20)
    expertid = models.CharField(db_column='expertID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    head_url = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


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
