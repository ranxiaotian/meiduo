"""
用户管理

    用户展示    --  获取用户信息,实现分页和搜索功能
        1. 先实现用户查询
            1.1 查询所有用户
            1.2 将对象列表转换为 满足需求的字典列表 (序列化器)
            1.3 返回响应
        2. 最后实现分页
        3. 再实现搜索功能

    新增用户    --  增加一个测试用户

"""
from rest_framework.views import APIView        # 基类

from rest_framework.generics import GenericAPIView      # mixin

from rest_framework.generics import ListAPIView,RetrieveAPIView     # get
from apps.users.models import User
from apps.meiduo_admin.serializers.user import UserModelSerializer
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict

class PageNum(PageNumberPagination):

    # 1.开启分页
    # 2.设置默认每页多少条记录
    page_size = 5

    # 1. 开启 每页多少条记录 可以通过传递的参数传递
    # 2. pagesize=xxx 每页多少条记录的 key
    page_size_query_param = 'pagesize'

    #最大一页多少条记录
    max_page_size = 20

    def get_paginated_response(self, data):
        # self.page.paginator.per_page  动态
        # self.page_size 固定
        return Response(OrderedDict([
            ('count', self.page.paginator.count),           # 总共多少条记录
            ('lists', data),                                # 结果列表
            ('page', self.page.number),                     # 第几页
            ('pages', self.page.paginator.num_pages),       # 总共几页
            ('pagesize', self.page.paginator.per_page)      # 一页多少条记录
        ]))


class UserAPIView(ListAPIView):

    queryset = User.objects.all()

    serializer_class = UserModelSerializer

    pagination_class = PageNum
