from rest_framework import serializers

from apps.products.models import Product, WishList
from apps.users.serializers import ReadUserSerializer


class ProductSerializer(serializers.ModelSerializer):
    added_in_wishlist = serializers.IntegerField(source='added_in_wishlist_by', read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('name', 'products')


class DetailWishListSerializer(WishListSerializer):
    products = ProductSerializer(many=True)


class AdminWishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = ('name', 'products', 'user')


class AdminDetailWishListSerializer(AdminWishListSerializer):
    products = ProductSerializer(many=True)
    user = ReadUserSerializer()
