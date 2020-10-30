

"""
日活用户

当天登录的用户的总量
2020-10-30  10:10:10
2020-10-30  15:10:10

2020-10-30  00:00:00
"""
from apps.users.models import User
from datetime import date
from rest_framework.response import Response


from rest_framework.views import APIView
# 基类
from rest_framework.generics import GenericAPIView
# 一般和Mixin配合使用      mixin(增删改查)
from rest_framework.generics import ListAPIView,RetrieveAPIView
# 三级视图 已经继承了Mixin http方法都不用写了


class DailyActiveAPIView(APIView):

    def get(self,request):

        today = date.today()
        count = User.objects.filter(last_login__gte=today).count()

        return Response({'count':count})


"""
日下单用户量统计


"""
class DailyOrderCountAPIView(APIView):

    def get(self,request):
        today=date.today()
        count=User.objects.filter(orderinfo__create_time__gte=today).count()
        return Response({'count':count})