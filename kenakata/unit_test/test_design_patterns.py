from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.builders.order_builder import OrderBuilder
from core.models import Address, Cart, CartItem, Category, Product, Vendor
from core.payments.factory import FactoryRegistry, PaymentFactory
from core.strategies.shipping import StandardShippingStrategy


class DesignPatternIntegrationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='pattern-user', email='pattern@example.com', password='secret123')

        self.vendor = Vendor.objects.create(
            user=self.user,
            name='Test Vendor',
            email='vendor@example.com',
            phone='123456789',
            address='Vendor address'
        )
        self.category = Category.objects.create(title='Test Category')
        self.product = Product.objects.create(
            vendor=self.vendor,
            category=self.category,
            title='Pattern Product',
            description='Desc',
            price=Decimal('150.00'),
            stock=10,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.address = Address.objects.create(
            user=self.user,
            title='Home',
            address_line='123 Main St',
            city='Dhaka',
            state='Dhaka',
            postal_code='1212',
            country='Bangladesh',
            phone='01700000000',
            is_default=True,
        )

    def test_standard_shipping_strategy_applies_free_shipping_threshold(self):
        strategy = StandardShippingStrategy()
        self.assertEqual(strategy.calculate(Decimal('250.00')), Decimal('4.99'))
        self.assertEqual(strategy.calculate(Decimal('301.00')), Decimal('0.00'))

    def test_order_builder_creates_order_and_items(self):
        builder = OrderBuilder()
        total = Decimal('300.00')
        order = (
            builder.set_user(self.user)
            .set_shipping_address(self.address)
            .set_total(total)
            .add_cart_items(self.cart.items.all())
            .set_status('Pending')
            .build()
        )

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.total_amount, total)
        self.assertEqual(order.status, 'Pending')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product, self.product)

    def test_payment_factory_uses_singleton_registry(self):
        registry_one = FactoryRegistry.get_instance()
        registry_two = FactoryRegistry.get_instance()

        self.assertIs(registry_one, registry_two)

        factory = registry_one.get_factory('Card')
        self.assertIsInstance(factory, PaymentFactory)

        processor = factory.create_payment()

        self.assertTrue(hasattr(processor, 'pay'))
        self.assertTrue(processor.pay(Decimal('100.00')))
