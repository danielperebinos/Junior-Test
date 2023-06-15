from django.db import models
from rest_framework.generics import get_object_or_404


class Product(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'sku'], name='unique_product_name_sku'
            )
        ]

    name = models.CharField(max_length=250, null=False)
    price = models.FloatField(null=False)
    sku = models.CharField(max_length=8, null=False)
    description = models.TextField(null=True)


class WishList(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'user'], name='unique_wishlist_name_user'
            )
        ]

    name = models.CharField(max_length=250, null=False)
    user = models.ForeignKey('users.user', on_delete=models.CASCADE)
    products = models.ManyToManyField('products.product')
