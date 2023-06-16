from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.products.models import Product, WishList


class ProductSerializer(serializers.ModelSerializer):
    added_in_wishlist = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, price):
        if (isinstance(price, float) or isinstance(price, int)) and price >= 0:
            return price

        raise ValidationError('Wrong price!')


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'name', 'products')


class WishListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList.products.through
        fields = "__all__"


class DetailWishListSerializer(WishListSerializer):
    products = ProductSerializer(many=True)


class NameWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('id', 'name')
