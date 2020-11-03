from rest_framework.viewsets import ModelViewSet
from apps.orders.models import OrderInfo
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializers.order import OrderSeriazlier
from rest_framework.views import APIView
from rest_framework.response import Response

class OrdersView(ModelViewSet):
    serializer_class = OrderSeriazlier
    queryset = OrderInfo.objects.all()
    pagination_class = PageNum


class OrderStatusAPIView(APIView):
    # 在视图中定义status方法修改订单状态

    def put(self, request, order_id):
        # 获取订单对象
        order = OrderInfo.objects.get(order_id=order_id)
        # 获取要修改的状态值
        status = request.data.get('status')
        # 修改订单状态
        order.status = status
        order.save()
        return Response({
            'order_id': order.order_id,
            'status': status
        })
