from rest_framework.routers import SimpleRouter

from apps.products.views import ProductsViewSet, WishListViewSet

products = SimpleRouter()
products.register(r'products', ProductsViewSet)
products.register(r'wishlist', WishListViewSet)

urlpatterns = products.urls
