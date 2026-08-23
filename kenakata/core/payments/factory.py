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


class PaymentFactory:
    _instance = None
    _registry = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._register_default_processors()
        return cls._instance

    @classmethod
    def get_instance(cls):
        return cls()

    def _register_default_processors(self):
        self.register('Card', CardProvider, CardPaymentAdapter)
        self.register('Credit / Debit Card', CardProvider, CardPaymentAdapter)
        self.register('PayPal', CardProvider, CardPaymentAdapter)
        self.register('Apple Pay', CardProvider, CardPaymentAdapter)
        self.register('bKash', BkashProvider, BkashPaymentAdapter)
        self.register('Nagad', NagadProvider, NagadPaymentAdapter)
        self.register('Cash on Delivery', CashOnDeliveryProvider, CashOnDeliveryPaymentAdapter)

    @classmethod
    def register(cls, name, provider_class, adapter_class):
        cls._registry[name] = {'provider': provider_class, 'adapter': adapter_class}

    @classmethod
    def create(cls, name):
        factory = cls.get_instance()
        config = factory._registry.get(name)
        if not config:
            raise ValueError(f'Unsupported payment method: {name}')
        provider = config['provider']()
        adapter = config['adapter'](provider)
        return adapter

    @classmethod
    def available_methods(cls):
        return list(cls._registry.keys())
