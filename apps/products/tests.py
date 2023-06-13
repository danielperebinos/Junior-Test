from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.products.models import Product, WishList
from apps.products.serializers import ProductSerializer, DetailWishListSerializer
from apps.users.models import User


class TestProductsView(TestCase):
    fixtures = ['FixtureProducts', 'FixtureUsers', 'FixtureWishlist']

    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.filter(username='daniel').first()
        self.client.force_authenticate(user=self.test_user)

    def test_list_products(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = ProductSerializer(Product.objects.all(), many=True).data
        self.assertEqual(response.data, data)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = ProductSerializer(Product.objects.filter(id=1).first()).data
        self.assertEqual(response.data, data)

    def test_update_product(self):
        pk = 1
        url = reverse('product-detail', args=[pk])
        data = {
            'name': 'changed product',
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.filter(pk=pk).first().name, data['name'])

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'name': 'test product',
            'price': 10,
            'sku': '12345678',
            'description': 'test description'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Product.objects.filter(**data).exists())

    def test_delete_product(self):
        pk = 1
        url = reverse('product-detail', args=[pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Product.objects.filter(pk=pk).exists())


class WishListViewSet(TestCase):
    fixtures = ['FixtureProducts', 'FixtureUsers', 'FixtureWishlist']

    def setUp(self):
        self.client = APIClient()
        self.test_user = User.objects.filter(username='daniel').first()
        self.client.force_authenticate(user=self.test_user)

    def test_list_wishlist(self):
        url = reverse('wishlist-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = DetailWishListSerializer(WishList.objects.filter(user=self.test_user), many=True).data
        self.assertEqual(response.data, data)

    def test_retrieve_wishlist(self):
        url = reverse('wishlist-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = DetailWishListSerializer(WishList.objects.filter(id=1, user=self.test_user).first()).data
        self.assertEqual(response.data, data)

    def test_update_wishlist(self):
        pk = 1
        url = reverse('wishlist-detail', args=[pk])
        data = {
            'name': 'changed wishlist',
            'products': [1, 2, 3]
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WishList.objects.filter(pk=pk, user=self.test_user).first().name, data['name'])
        self.assertEqual(list(WishList.objects.filter(pk=pk, user=self.test_user).first().products.values_list('id', flat=True)), data['products'])

    def test_create_wishlist(self):
        url = reverse('wishlist-list')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WishList.objects.last().user, self.test_user)

    def test_delete_wishlist(self):
        pk = 1
        url = reverse('wishlist-detail', args=[pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(WishList.objects.filter(pk=pk).exists())

    def test_add_product(self):
        pk = 1
        url = reverse('wishlist-add-product', args=[pk])
        data = {
            'name': '4'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WishList.objects.filter(pk=1).first().products.filter(name='4').exists())

    def test_remove_product(self):
        pk = 1
        url = reverse('wishlist-remove-product', args=[pk])
        data = {
            'name': '1'
        }
        response = self.client.delete(url, data=data)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(WishList.objects.filter(pk=1).first().products.filter(name='1').exists())
