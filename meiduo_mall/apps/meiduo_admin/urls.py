# from rest_framework_jwt.views import obtain_jwt_token
from django.urls import path
from apps.meiduo_admin.user import meiduo_token
from apps.meiduo_admin.views import home,user,images,sku
from apps.meiduo_admin.views import permissions
from apps.meiduo_admin.views import order
from apps.meiduo_admin.views import specs,spu,option,brand

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


    #
    path('skus/categories/',sku.GoodsCategoryAPIView.as_view()),

    #sku 中获取 spu的数据
    path('goods/simple/', sku.SPUListAPIView.as_view()),

    #sku 中获取 spu的规格和规格选项
    path('goods/<spu_id>/specs/', sku.SPUSpecAPIView.as_view()),

    #权限中 获取 ContentType 的数据
    path('permission/content_types/', permissions.ConentTypeListAPIView.as_view()),

    #组中 获取 权限列表数据
    path('permission/simple/', permissions.GroupPermissionListAPIView.as_view()),

    #组中 获取 权限列表数据
    path('permission/groups/simple/', permissions.SimpleGroupListAPIView.as_view()),

    # 用户总量统计
    path('statistical/total_count/',home.UserTotalCountView.as_view()),
    path('statistical/day_increment/',home.UserDailyActiveCountView.as_view()),

    #订单状态
    path('orders/<order_id>/status/',order.OrderStatusAPIView.as_view()),

# 商品作业
    path('goods/brands/simple/', spu.SPUBrandView.as_view()),
    path('goods/channel/categories/', spu.ChannelCategorysView.as_view()),
    path('goods/channel/categories/<int:pk>/', spu.ChannelCategoryView.as_view()),
    path('goods/specs/simple/', option.OptionSimple.as_view()),

]

from rest_framework.routers import DefaultRouter
#  1.创建router实例
rouer=DefaultRouter()
# 2. 设置路由
rouer.register('skus/images',images.ImageModelViewSet,basename='images')



################sku#############################
rouer.register('skus',sku.SKUModelViewSet,basename='skus')



###############权限##################################
rouer.register('permission/perms',permissions.PermissionModelViewSet,basename='perms')

###############组##################################
rouer.register('permission/groups',permissions.GroupModelViewSet,basename='groups')

###############普通管理员##################################
rouer.register('permission/admins',permissions.AdminUserModelViewSet,basename='admins')

# 作业订单管理
rouer.register('orders',order.OrdersView,basename='orders')

# 商品作业
# 商品规格
rouer.register(r'goods/specs', specs.SpecsView, basename='spu')


#商品品牌
rouer.register(r'goods/brands', brand.BrandsView, basename='brands')


#spu
rouer.register(r'goods', spu.SPUGoodsView, basename='goods')


#商品选项
rouer.register(r'specs/options', option.OptionsView, basename='specs')


# 3.追加到 urlpatterns
urlpatterns+=rouer.urls