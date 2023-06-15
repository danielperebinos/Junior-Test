from rest_framework.routers import SimpleRouter

from apps.products.views import ProductsViewSet, WishListViewSet

products = SimpleRouter(trailing_slash=False)
products.register(r'products', ProductsViewSet)
products.register(r'wishlist', WishListViewSet)

urlpatterns = products.urls
