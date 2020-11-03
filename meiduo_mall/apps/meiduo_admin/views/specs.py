from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.serializers.specs import SPUSpecificationSerializer
class SpecsView(ModelViewSet):

    serializer_class = SPUSpecificationSerializer
    queryset = SPUSpecification.objects.all()
    pagination_class = PageNum