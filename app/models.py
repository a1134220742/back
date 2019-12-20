# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrator(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrator'


class Applicationforexpert(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    real_name = models.CharField(max_length=45, blank=True, null=True)
    id_number = models.CharField(db_column='ID_number', max_length=45, blank=True, null=True)  # Field name made lowercase.
    institution = models.CharField(max_length=45, blank=True, null=True)
    credentials_url = models.CharField(max_length=100, blank=True, null=True)
    expert_name = models.CharField(max_length=45, blank=True, null=True)
    expert_unit = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'applicationForExpert'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ChatList(models.Model):
    sender_name = models.CharField(max_length=20)
    receiver_name = models.CharField(max_length=20)
    date = models.DateTimeField()
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chat_list'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    expert_id = models.CharField(max_length=45, blank=True, null=True)
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
