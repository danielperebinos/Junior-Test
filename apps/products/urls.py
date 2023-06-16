from rest_framework.routers import SimpleRouter

from apps.products.views import ProductsViewSet, WishListProductViewSet, WishListViewSet

products = SimpleRouter(trailing_slash=False)
products.register(r'products', ProductsViewSet)
products.register(r'wishlist/products', WishListProductViewSet, basename='wishlist-products')
products.register(r'wishlist', WishListViewSet)

urlpatterns = products.urls
