from rest_framework.viewsets import ModelViewSet
from apps.goods.models import SKU
from apps.meiduo_admin.serializers.sku import SKUModelSerializer
from apps.meiduo_admin.utils import PageNum

class SKUModelViewSet(ModelViewSet):

    # queryset = SKU.objects.all()
    def get_queryset(self):

        keyword=self.request.query_params.get('keyword')
        if keyword:
            return SKU.objects.filter(name__contains=keyword)

        return SKU.objects.all()


    serializer_class = SKUModelSerializer

    pagination_class = PageNum