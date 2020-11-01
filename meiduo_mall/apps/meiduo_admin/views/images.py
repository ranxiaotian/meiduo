from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKUImage
from apps.meiduo_admin.serializers.images import SKUImageModelSerializer
from apps.meiduo_admin.utils import PageNum

class ImageModelViewSet(ModelViewSet):

    queryset = SKUImage.objects.all()

    serializer_class = SKUImageModelSerializer

    pagination_class = PageNum