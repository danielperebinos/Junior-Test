from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=250, null=False)
    price = models.FloatField(null=False)
    sku = models.CharField(max_length=8, null=False)
    description = models.TextField(null=True)

    @property
    def added_in_wishlist_by(self):
        return WishList.objects.filter(products=self).values('user').distinct().count()


class WishList(models.Model):
    name = models.CharField(max_length=250, null=False)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.product', default=None, null=True, blank=True)