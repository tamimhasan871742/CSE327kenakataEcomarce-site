from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import Order, Wishlist, Review, Address, PaymentMethod, Product, OrderItem

User = get_user_model()


class TestAccountView(TestCase):

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            email="user@example.com",
            username="testuser",
            password="testpass"
        )

        # Login client
        self.client = Client()
        self.client.login(email="user@example.com", password="testpass")

        # Products
        self.product1 = Product.objects.create(title="Product1", price=100)
        self.product2 = Product.objects.create(title="Product2", price=200)

        # Order and items
        self.order = Order.objects.create(user=self.user, total_amount=300)
        self.order_item1 = OrderItem.objects.create(order=self.order, product=self.product1, quantity=1, price=100)
        self.order_item2 = OrderItem.objects.create(order=self.order, product=self.product2, quantity=1, price=200)

        # Wishlist
        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist.products.add(self.product1)

        # Review
        self.review = Review.objects.create(user=self.user, product=self.product1, rating=5, comment="Great product!")

        # Address
        self.address = Address.objects.create(
            user=self.user,
            title="Home",
            address_line="123 Street",
            city="City",
            state="State",
            postal_code="12345",
            country="Country",
            phone="1234567890"
        )

        # Payment
        self.payment = PaymentMethod.objects.create(
            user=self.user,
            card_number="1234567812345678",
            card_name="Test User",
            expiry_date="2030-12-31",
            is_default=True
        )

    # TESTS 
    def test_account_view_status_code_and_template(self):
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')

    def test_account_view_context(self):
        response = self.client.get(reverse('account'))
        context = response.context

        self.assertEqual(context['user'], self.user)
        self.assertIn(self.order, context['orders'])
        self.assertEqual(context['wishlist'], self.wishlist)
        self.assertIn(self.review, context['reviews'])
        self.assertIn(self.address, context['addresses'])
        self.assertIn(self.payment, context['payments'])
        self.assertIn(self.product1, context['products_ordered'])
        self.assertIn(self.product2, context['products_ordered'])

    def test_account_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

   
    def test_account_view_empty_related_objects(self):
        
        user2 = User.objects.create_user(email="newuser@example.com", username="newuser", password="pass")
        self.client.logout()
        self.client.login(email="newuser@example.com", password="pass")
        response = self.client.get(reverse('account'))
        context = response.context

        self.assertEqual(list(context['orders']), [])
        self.assertIsNone(context['wishlist'])
        self.assertEqual(list(context['reviews']), [])
        self.assertEqual(list(context['addresses']), [])
        self.assertEqual(list(context['payments']), [])
        self.assertEqual(list(context['products_ordered']), [])

   
    def test_account_view_fail_wrong_order_check(self):
        response = self.client.get(reverse('account'))
        context = response.context

        
        fake_product = Product(title="Fake", price=0)
        self.assertIn(fake_product, context['products_ordered'])  

    def test_account_view_fail_wrong_wishlist(self):
        response = self.client.get(reverse('account'))
        context = response.context

        
        self.assertIsNone(context['wishlist'])  

    def test_account_view_fail_order_count(self):
        response = self.client.get(reverse('account'))
        context = response.context

        
        self.assertEqual(len(context['orders']), 0)  
