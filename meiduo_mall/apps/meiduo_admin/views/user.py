"""
用户管理

    用户展示    --  获取用户信息,实现分页和搜索功能
        1. 先实现用户查询
            1.1 查询所有用户
            1.2 将对象列表转换为 满足需求的字典列表 (序列化器)
            1.3 返回响应
        2. 再实现搜索功能
        3. 最后实现分页

    新增用户    --  增加一个测试用户

"""
from rest_framework.views import APIView        # 基类

from rest_framework.generics import GenericAPIView      # mixin

from rest_framework.generics import ListAPIView,RetrieveAPIView     # get
from apps.users.models import User
from apps.meiduo_admin.serializers.user import UserModelSerializer

class UserAPIView(ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserModelSerializer
