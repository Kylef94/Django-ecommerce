from django.test import TestCase
from django.db.utils import IntegrityError
from datetime import date
from shop.models import Product, Category, Discount, Order, OrderItem
from accounts.models import Customer

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name='Test Product',
            price=19.99,
            description='This is a test product.',
            qty_in_stock=10,
            slug='test-product',
            picture='test.jpg',
        )
        self.assertEqual(str(product), "Name: Test Product")

    def test_product_required_fields(self):
        with self.assertRaises(IntegrityError):
            product = Product.objects.create(name='Incomplete Product')

class CategoryModelTest(TestCase):
    def test_category_creation(self):
        category = Category.objects.create(
            name='Test Category',
            slug='test-category',
        )
        self.assertEqual(str(category), "Name: Test Category")

class DiscountModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Discounted Product',
            price=29.99,
            description='This product has a discount.',
            qty_in_stock=5,
            slug='discounted-product',
        )

    def test_discount_creation(self):
        discount = Discount.objects.create(
            product=self.product,
            promo='TEST123',
            start=date.today(),
            end=date.today(),
            amount=5.00,
        )
        self.assertEqual(str(discount), "Promo Name: TEST123\nProduct: Discounted Product\nAmount: 5.0")

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email='testuser@test.com')
        
    def test_order_creation(self):
        order = Order.objects.create(
            customer=self.customer,
            complete=False,
            txn_id='123456',
        )
        self.assertEqual(str(order), str(order.id))

    def test_order_total_calculation(self):
        product = Product.objects.create(
            name='Order Test Product',
            price=10.00,
            description='Product for order total calculation.',
            qty_in_stock=5,
            slug='order-test-product',
        )
        order = Order.objects.create(
            customer=self.customer,
            complete=False,
            txn_id='654321',
        )
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=3,
        )
        self.assertEqual(order.get_total, 30.00)

class OrderItemModelTest(TestCase):
    def test_order_item_total_calculation(self):
        product = Product.objects.create(
            name='Order Item Test Product',
            price=15.00,
            description='Product for order item total calculation.',
            qty_in_stock=8,
            slug='order-item-test-product',
        )
        order = Order.objects.create(
            complete=False,
            txn_id='987654',
        )
        order_item = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=2,
        )
        self.assertEqual(order_item.get_item_total, 30.00)
