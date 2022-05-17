from rest_framework import serializers
from apps.goods.models import SpecificationOption

class OptionSerialzier(serializers.ModelSerializer):
    # 嵌套返回规格名称
    spec = serializers.StringRelatedField(read_only=True)
    # 返回规格id
    spec_id = serializers.IntegerField()

    class Meta:
        model = SpecificationOption  # 规格选项表中的spec字段关联了规格表
        fields = "__all__"

from apps.goods.models import SPUSpecification
class OptionSpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model=SPUSpecification
        fields='__all__'