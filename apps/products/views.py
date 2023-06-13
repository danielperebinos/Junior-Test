from drf_util.decorators import serialize_decorator
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema, no_body

from apps.products.models import Product, WishList
from apps.products.serializers import ProductSerializer, WishListSerializer, DetailWishListSerializer, AdminDetailWishListSerializer, AdminWishListSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class WishListViewSet(ModelViewSet):
    queryset = WishList.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = WishListSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DetailWishListSerializer
        else:
            return WishListSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    @swagger_auto_schema(request_body=no_body)
    def create(self, request, *args, **kwargs):
        new_wishlist = WishList.objects.create(user=request.user)
        return Response(self.serializer_class(new_wishlist).data)

    @swagger_auto_schema(request_body=ProductSerializer)
    @serialize_decorator(ProductSerializer, partial=True)
    @action(detail=True, methods=['delete'], name='remove-product')
    def remove_product(self, request, *args, **kwargs):
        if request.valid:
            products = Product.objects.filter(**request.valid).first()
            wishlist = self.get_object()
            wishlist.products.remove(products)
            wishlist.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=ProductSerializer)
    @serialize_decorator(ProductSerializer, partial=True)
    @action(detail=True, methods=['post'], name='add-product')
    def add_product(self, request, *args, **kwargs):
        if request.valid:
            products = Product.objects.filter(**request.valid).first()
            wishlist = self.get_object()
            wishlist.products.add(products)
            wishlist.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)