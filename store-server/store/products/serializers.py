from rest_framework import serializers

from products.models import Product, ProductCategory, Basket


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('name', 'description')

class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user', 'product', 'quantity', 'created_timestamp', 'objects')
