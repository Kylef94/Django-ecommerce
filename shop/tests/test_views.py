from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product, Order, OrderItem

class ShopViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            name='Test Product',
            price=19.99,
            description='This is a test product.',
            qty_in_stock=10,
            slug='test-product',
            picture='test.jpg',
        )
        self.order = Order.objects.create(customer=self.user, complete=False)
        self.order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_products_view(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/products.html')
        self.assertEqual(len(response.context['product_list']), 1)

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        self.assertEqual(response.context['object'], self.product)

    def test_cart_view_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/cart.html')
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['order'], self.order)

    def test_cart_view_unauthenticated_user(self):
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/cart.html')
        self.assertEqual(len(response.context['items']), 0)
        self.assertEqual(response.context['order']['get_total'], 0)
        self.assertEqual(response.context['order']['get_total_qty'], 0)

    def test_update_item_view(self):
        data = {'productId': self.product.id, 'action': 'add'}
        response = self.client.post(reverse('update_item'), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Item was added')

    def test_checkout_view_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/checkout.html')
        self.assertEqual(len(response.context['items']), 1)
        self.assertEqual(response.context['order'], self.order)
        self.assertIsNotNone(response.context['custform'])
        self.assertIsNotNone(response.context['addrform'])

    def test_checkout_view_unauthenticated_user(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/checkout.html')
        self.assertEqual(len(response.context['items']), 0)
        self.assertEqual(response.context['order']['get_total'], 0)
        self.assertEqual(response.context['order']['get_total_qty'], 0)
        self.assertIsNotNone(response.context['custform'])
        self.assertIsNotNone(response.context['addrform'])