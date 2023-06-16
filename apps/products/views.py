from django.db.models import Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import mixins, status

from apps.products.models import Product, WishList
from apps.products.serializers import ProductSerializer, WishListSerializer, DetailWishListSerializer, NameWishListSerializer, WishListProductSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all().annotate(
        added_in_wishlist=Count('wishlist')
    ).prefetch_related('wishlist_set')

    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = (IsAuthenticated,)
        else:
            self.permission_classes = (IsAdminUser,)
        return super().get_permissions()


class WishListViewSet(ModelViewSet):
    queryset = WishList.objects.all().prefetch_related('products')
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


class WishListProductViewSet(mixins.CreateModelMixin,GenericViewSet):
    queryset = WishList.products.through.objects.all()
    serializer_class = WishListProductSerializer

    def get_queryset(self):
        return self.queryset.filter(wishlist__user_id=self.request.user)

    @swagger_auto_schema(request_body=WishListProductSerializer)
    @action(detail=False, methods=['delete'], name='remove-product')
    def delete(self, request, *args, **kwargs):
        self.queryset.filter(product_id=request.data.get('product'), wishlist_id=request.data.get('wishlist')).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
