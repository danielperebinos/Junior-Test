from django.db.models import Count
from drf_util.decorators import serialize_decorator
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

from apps.products.models import Product, WishList
from apps.products.serializers import ProductSerializer, WishListSerializer, DetailWishListSerializer, NameWishListSerializer, IdProductSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all().annotate(
        added_in_wishlist=Count('wishlist')
    )

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
        elif self.action == 'create':
            return NameWishListSerializer
        else:
            return WishListSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(request_body=IdProductSerializer)
    @action(detail=True, methods=['delete'], name='remove-product', url_path='remove-product')
    def remove_product(self, request, *args, **kwargs):
        wishlist = self.get_object()
        wishlist.products.remove(request.data.get('product_id'))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(request_body=IdProductSerializer)
    @action(detail=True, methods=['post'], name='add-product', url_path='add-product')
    def add_product(self, request, *args, **kwargs):
        wishlist = self.get_object()
        wishlist.products.add(request.data.get('product_id'))
        return Response(status=status.HTTP_200_OK)
