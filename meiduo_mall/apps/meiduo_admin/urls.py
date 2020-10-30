# from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from apps.meiduo_admin.user import meiduo_token
from apps.meiduo_admin.views import home
urlpatterns = [
    # path('authorizations/',obtain_jwt_token),
    path('authorizations/',meiduo_token),

    # 日活统计
    path('statistical/day_active/',home.DailyActiveAPIView.as_view()),
    # 日下单用户
    path('statistical/day_orders/',home.DailyOrderCountAPIView.as_view()),
]