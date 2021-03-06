# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

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
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
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


class CompleteEnrollmentData(models.Model):
    identifier = models.IntegerField(blank=True, null=True)
    major1 = models.TextField(blank=True, null=True)
    major2 = models.TextField(blank=True, null=True)
    minor1 = models.TextField(blank=True, null=True)
    minor2 = models.TextField(blank=True, null=True)
    term = models.TextField(blank=True, null=True)
    term_number = models.IntegerField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'complete_enrollment_data'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class EnrollmentData1100(models.Model):
    identifier = models.IntegerField(blank=True, null=True)
    student_year = models.IntegerField(blank=True, null=True)
    major_1 = models.TextField(blank=True, null=True)
    major_2 = models.TextField(blank=True, null=True)
    minor_1 = models.TextField(blank=True, null=True)
    minor_2 = models.TextField(blank=True, null=True)
    term = models.TextField(blank=True, null=True)
    term_number = models.IntegerField(blank=True, null=True)
    subject = models.TextField(blank=True, null=True)
    subject_title = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'enrollment_data_1100'


class EnrollmentDataUpdated(models.Model):
    identifier = models.IntegerField()
    year = models.IntegerField()
    major_1 = models.TextField()
    major_2 = models.TextField(blank=True, null=True)
    minor_1 = models.TextField(blank=True, null=True)
    minor_2 = models.TextField(blank=True, null=True)
    term = models.TextField()
    term_number = models.IntegerField()
    subject = models.TextField()
    subject_title = models.TextField()

    class Meta:
        managed = False
        db_table = 'enrollment_data_updated'


class SharedClassesByMajor(models.Model):
    major = models.TextField(blank=True, null=True)
    matrix = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'shared_classes_by_major'


class SubjectInfo(models.Model):
    subject = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    prereqs = models.TextField(blank=True, null=True)
    units = models.TextField(blank=True, null=True)
    optional = models.TextField(blank=True, null=True)
    instructors = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)  # This field type is a guess.
    term1 = models.IntegerField(blank=True, null=True)
    term2 = models.IntegerField(blank=True, null=True)
    term3 = models.IntegerField(blank=True, null=True)
    term4 = models.IntegerField(blank=True, null=True)
    term5 = models.IntegerField(blank=True, null=True)
    term6 = models.IntegerField(blank=True, null=True)
    term7 = models.IntegerField(blank=True, null=True)
    term8 = models.IntegerField(blank=True, null=True)
    term9 = models.IntegerField(blank=True, null=True)
    term10 = models.IntegerField(blank=True, null=True)
    term11 = models.IntegerField(blank=True, null=True)
    term12 = models.IntegerField(blank=True, null=True)
    term13 = models.IntegerField(blank=True, null=True)
    term14 = models.IntegerField(blank=True, null=True)
    term15 = models.IntegerField(blank=True, null=True)
    term16 = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subject_info'
