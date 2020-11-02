
#####################权限#################################
from rest_framework import serializers
from django.contrib.auth.models import Permission


class PermissionModelSerializer(serializers.ModelSerializer):

    class Meta:
        model=Permission
        fields='__all__'
