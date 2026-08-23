from abc import ABC, abstractmethod


class PaymentAdapter(ABC):
    @abstractmethod
    def pay(self, amount):
        raise NotImplementedError


class CardPaymentAdapter(PaymentAdapter):
    def __init__(self, provider):
        self.provider = provider

    def pay(self, amount):
        return self.provider.charge(amount)


class BkashPaymentAdapter(PaymentAdapter):
    def __init__(self, provider):
        self.provider = provider

    def pay(self, amount):
        return self.provider.send_payment(amount)


class NagadPaymentAdapter(PaymentAdapter):
    def __init__(self, provider):
        self.provider = provider

    def pay(self, amount):
        return self.provider.make_transaction(amount)


class CashOnDeliveryPaymentAdapter(PaymentAdapter):
    def __init__(self, provider):
        self.provider = provider

    def pay(self, amount):
        return self.provider.collect(amount)
