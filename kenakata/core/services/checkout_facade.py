from decimal import Decimal

from core.builders.order_builder import OrderBuilder
from core.models import Address
from core.observers.order_observers import DjangoMessageObserver
from core.observers.subject import Subject
from core.payments.factory import PaymentFactory
from core.strategies.shipping import calculate_shipping


class CheckoutFacade:
    def process_checkout(self, user, request, payment_method='Card'):
        from core.models import Cart

        cart = Cart.objects.filter(user=user).first()
        if not cart or not cart.items.exists():
            return {'success': False, 'message': 'Your cart is empty!'}

        address = Address.objects.filter(user=user, is_default=True).first()
        if not address:
            return {'success': False, 'message': 'Please add a default shipping address.'}

        subtotal = sum(item.get_total() for item in cart.items.all())
        shipping = calculate_shipping(subtotal, request.session.get('shipping'))
        tax = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'))
        discount = Decimal('0')
        total = (subtotal + shipping + tax - discount).quantize(Decimal('0.01'))

        try:
            payment_processor = PaymentFactory.create(payment_method)
            payment_result = payment_processor.pay(total)
        except ValueError:
            return {'success': False, 'message': 'Invalid payment method selected.'}

        if not payment_result:
            return {'success': False, 'message': 'Payment processing failed.'}

        order = (
            OrderBuilder()
            .set_user(user)
            .set_shipping_address(address)
            .set_total(total)
            .add_cart_items(cart.items.all())
            .set_status('Pending')
            .build()
        )

        subject = Subject()
        subject.attach(DjangoMessageObserver(request))
        subject.notify(order, 'order_created')

        cart.items.all().delete()
        return {'success': True, 'order': order, 'total': total, 'shipping': shipping, 'tax': tax}
