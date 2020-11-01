from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage
from apps.meiduo_admin.serializers.images import SKUImageModelSerializer
from apps.meiduo_admin.utils import PageNum

class ImageModelViewSet(ModelViewSet):

    queryset = SKUImage.objects.all()

    serializer_class = SKUImageModelSerializer

    pagination_class = PageNum


###########################获取所有sku的功能
from apps.goods.models import SKU
from rest_framework.generics import GenericAPIView
from apps.meiduo_admin.serializers.images import ImageSKUModelSerializer
from rest_framework.mixins import ListModelMixin
class ImageSKUAPIView(ListModelMixin,GenericAPIView):

    queryset = SKU.objects.all()

    serializer_class = ImageSKUModelSerializer

    def get(self,request):
        return self.list(request)
        # skus=self.get_queryset()
        #
        # serializer=self.get_serializer(skus,many=True)
        #
        # return Response(serializer.data)


from rest_framework.generics import ListAPIView

