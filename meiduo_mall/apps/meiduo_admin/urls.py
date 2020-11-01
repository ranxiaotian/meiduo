# from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from apps.meiduo_admin.user import meiduo_token
from apps.meiduo_admin.views import home,user,images,sku

urlpatterns = [
    # path('authorizations/',obtain_jwt_token),
    path('authorizations/',meiduo_token),

    # 日活统计
    path('statistical/day_active/',home.DailyActiveAPIView.as_view()),
    # 日下单用户
    path('statistical/day_orders/',home.DailyOrderCountAPIView.as_view()),
    # 月增用户趋势图
    path('statistical/month_increment/',home.MonthCountAPIView.as_view()),


    # user
    path('users/',user.UserAPIView.as_view()),
    # 获取图片新增中的 sku展示
    path('skus/simple/',images.ImageSKUAPIView.as_view()),



]

from rest_framework.routers import DefaultRouter
#  1.创建router实例
rouer=DefaultRouter()
# 2. 设置路由
rouer.register('skus/images',images.ImageModelViewSet,basename='images')



################sku#############################
rouer.register('skus',sku.SKUModelViewSet,basename='skus')

# 3.追加到 urlpatterns
urlpatterns+=rouer.urls