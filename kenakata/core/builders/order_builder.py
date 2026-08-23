from decimal import Decimal

from core.models import Order, OrderItem


class OrderBuilder:
    def __init__(self):
        self.user = None
        self.shipping_address = None
        self.total_amount = Decimal('0')
        self.cart_items = []
        self.status = 'Pending'

    def set_user(self, user):
        self.user = user
        return self

    def set_shipping_address(self, address):
        self.shipping_address = address
        return self

    def set_total(self, total_amount):
        self.total_amount = Decimal(str(total_amount))
        return self

    def add_cart_items(self, cart_items):
        self.cart_items = list(cart_items)
        return self

    def set_status(self, status):
        self.status = status or 'Pending'
        return self

    def build(self):
        if not self.user:
            raise ValueError('Order user is required.')

        order = Order.objects.create(
            user=self.user,
            total_amount=self.total_amount,
            status=self.status,
        )

        for item in self.cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        return order
