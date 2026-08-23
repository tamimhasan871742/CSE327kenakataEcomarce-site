import logging

from django.contrib import messages

from core.observers.observer import Observer

logger = logging.getLogger(__name__)


class CustomerNotificationObserver(Observer):
    def update(self, order, event):
        if event == 'order_created':
            logger.info('Customer notified: order %s created', order.id)
        elif event == 'status_changed':
            logger.info('Customer notified: order %s status changed to %s', order.id, order.status)


class VendorNotificationObserver(Observer):
    def update(self, order, event):
        if event == 'order_created':
            logger.info('Vendor notified: new order %s created for user %s', order.id, order.user.username)
        elif event == 'status_changed':
            logger.info('Vendor notified: order %s updated to %s', order.id, order.status)


class AdminNotificationObserver(Observer):
    def update(self, order, event):
        logger.info('Admin notified: order %s event %s', order.id, event)


class DjangoMessageObserver(Observer):
    def __init__(self, request):
        self.request = request

    def update(self, order, event):
        if event == 'order_created':
            messages.success(self.request, '🎉 Your order has been placed successfully!')
        elif event == 'status_changed':
            messages.info(self.request, f'Order status updated to {order.status}.')
