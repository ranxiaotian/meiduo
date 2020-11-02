
# 用户
from apps.users.models import User
# 组
from django.contrib.auth.models import Group
# 权限
from django.contrib.auth.models import Permission

"""

1:1
1:n
n:m

老师和学生

老师表
学生表
老师和学生的关系表

"""


#####################权限#################################
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import Permission
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializers.permissions import PermissionModelSerializer

class PermissionModelViewSet(ModelViewSet):

    queryset = Permission.objects.all()

    serializer_class = PermissionModelSerializer

    pagination_class = PageNum