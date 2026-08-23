class CardProvider:
    def charge(self, amount):
        return True


class BkashProvider:
    def send_payment(self, amount):
        return True


class NagadProvider:
    def make_transaction(self, amount):
        return True


class CashOnDeliveryProvider:
    def collect(self, amount):
        return True
