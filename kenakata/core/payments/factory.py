from abc import ABC, abstractmethod

from core.payments.adapters import (
    BkashPaymentAdapter,
    CardPaymentAdapter,
    CashOnDeliveryPaymentAdapter,
    NagadPaymentAdapter,
)
from core.payments.processors import (
    BkashProvider,
    CardProvider,
    CashOnDeliveryProvider,
    NagadProvider,
)


# ============================================================
# Abstract Factory
# ============================================================

class PaymentFactory(ABC):
    """
    Abstract Factory.

    Each concrete payment factory is responsible for creating
    one specific type of payment product (adapter).
    """

    @abstractmethod
    def create_payment(self):
        """Create and return a payment adapter."""
        raise NotImplementedError

    @classmethod
    def create(cls, name):
        """
        Backward-compatible entry point used by the existing
        CheckoutFacade.

        It obtains the appropriate concrete factory from the
        Singleton FactoryRegistry and asks that factory to
        create the payment adapter.
        """
        factory = FactoryRegistry.get_instance().get_factory(name)

        if factory is None:
            raise ValueError(f'Unsupported payment method: {name}')

        return factory.create_payment()

    @classmethod
    def available_methods(cls):
        """Return all registered payment method names."""
        return FactoryRegistry.get_instance().available_methods()


# ============================================================
# Concrete Factories
# ============================================================

class CardPaymentFactory(PaymentFactory):
    """
    Concrete Factory for card-based payments.

    This covers:
    - Card
    - Credit / Debit Card
    - PayPal
    - Apple Pay
    """

    def create_payment(self):
        provider = CardProvider()
        return CardPaymentAdapter(provider)


class BkashPaymentFactory(PaymentFactory):
    """Concrete Factory for bKash payments."""

    def create_payment(self):
        provider = BkashProvider()
        return BkashPaymentAdapter(provider)


class NagadPaymentFactory(PaymentFactory):
    """Concrete Factory for Nagad payments."""

    def create_payment(self):
        provider = NagadProvider()
        return NagadPaymentAdapter(provider)


class CashOnDeliveryPaymentFactory(PaymentFactory):
    """Concrete Factory for Cash on Delivery payments."""

    def create_payment(self):
        provider = CashOnDeliveryProvider()
        return CashOnDeliveryPaymentAdapter(provider)


# ============================================================
# Singleton Factory Registry
# ============================================================

class FactoryRegistry:
    """
    Singleton registry that maps payment method names to
    concrete PaymentFactory objects.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._factories = {}
            cls._instance._register_default_factories()

        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def register_factory(self, name, factory):
        """
        Register a concrete PaymentFactory for a payment method.
        """
        if not isinstance(factory, PaymentFactory):
            raise TypeError(
                'factory must be an instance of PaymentFactory'
            )

        self._factories[name] = factory

    def get_factory(self, name):
        """
        Return the registered factory for the requested
        payment method.
        """
        return self._factories.get(name)

    def available_methods(self):
        """Return all registered payment method names."""
        return list(self._factories.keys())

    def _register_default_factories(self):
        """
        Register the application's default payment factories.

        The payment method names are intentionally kept exactly
        the same as the original implementation so that the
        existing website behavior does not change.
        """

        card_factory = CardPaymentFactory()
        bkash_factory = BkashPaymentFactory()
        nagad_factory = NagadPaymentFactory()
        cod_factory = CashOnDeliveryPaymentFactory()

        # Card-based payments
        self.register_factory('Card', card_factory)
        self.register_factory('Credit / Debit Card', card_factory)
        self.register_factory('PayPal', card_factory)
        self.register_factory('Apple Pay', card_factory)

        # Mobile financial services
        self.register_factory('bKash', bkash_factory)
        self.register_factory('Nagad', nagad_factory)

        # Cash payment
        self.register_factory('Cash on Delivery', cod_factory)
   
       
