from rest_framework.viewsets import ModelViewSet
from apps.meiduo_admin.utils import PageNum
from apps.meiduo_admin.serializers.option import OptionSerialzier
from apps.goods.models import SpecificationOption
class OptionsView(ModelViewSet):
    """
            规格选项表的增删改查
    """
    serializer_class = OptionSerialzier
    queryset = SpecificationOption.objects.all()
    pagination_class = PageNum

from rest_framework.generics import ListAPIView
from apps.goods.models import SPUSpecification
from apps.meiduo_admin.serializers.option import OptionSpecificationSerializer
class OptionSimple(ListAPIView):
    """
        获取规格信息
    """
    serializer_class = OptionSpecificationSerializer
    queryset = SPUSpecification.objects.all()
