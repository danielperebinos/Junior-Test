from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.products.models import Product, WishList
from apps.users.serializers import ReadUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    added_in_wishlist = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if (isinstance(price, float) or isinstance(price, int)) and price >= 0:
            return price

        raise ValidationError('Wrong price!')


class IdProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(allow_null=False)

    def validate_product_id(self, id):
        if Product.objects.filter(id=id).exists():
            return id
        raise ValidationError('Wrong product id!')


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'name', 'products')


class DetailWishListSerializer(WishListSerializer):
    products = ProductSerializer(many=True)


class NameWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'name')
