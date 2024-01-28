from rest_framework import serializers

from applications.billings.constants import CategoryChoices, SizeChoices
from applications.billings.models import Product
from applications.users.serializers import UserMdnTinySerializer


class ProductSerializer(serializers.ModelSerializer):
    user = UserMdnTinySerializer(read_only=True)
    category = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()
    expire_date = serializers.DateField(format='%Y-%m-%d')
    created = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)
    updated = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    def get_category(self, obj):
        return obj.get_category_display()

    def get_size(self, obj):
        return obj.get_size_display()

    def create(self, validated_data):
        context = self.context.get('context')

        return Product.objects.create(
            user=context.get('user'),
            category=CategoryChoices.CATEGORY_IN_DB.get(context.get('category')),
            size=SizeChoices.SIZE_IN_DB.get(context.get('size')),
            **validated_data
        )

    class Meta:
        model = Product
        fields = ['id', 'created', 'updated', 'category', 'price', 'cost', 'name', 'description',
                  'barcode', 'expire_date', 'size', 'user']
