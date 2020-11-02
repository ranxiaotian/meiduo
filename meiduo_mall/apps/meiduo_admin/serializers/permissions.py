
#####################权限#################################
from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Permission
        fields='__all__'


#####################ContentType#################################
from django.contrib.auth.models import ContentType

class ContentTypeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=ContentType
        fields=['id','name']

#####################组#################################
from django.contrib.auth.models import Group

class GroupModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Group
        fields='__all__'
