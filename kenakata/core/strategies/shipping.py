from abc import ABC, abstractmethod
from decimal import Decimal


class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, subtotal: Decimal) -> Decimal:
        raise NotImplementedError


class StandardShippingStrategy(ShippingStrategy):
    def calculate(self, subtotal: Decimal) -> Decimal:
        subtotal = Decimal(subtotal)
        if subtotal > Decimal('300'):
            return Decimal('0')
        return Decimal('4.99')


class ExpressShippingStrategy(ShippingStrategy):
    def calculate(self, subtotal: Decimal) -> Decimal:
        subtotal = Decimal(subtotal)
        if subtotal > Decimal('300'):
            return Decimal('0')
        return Decimal('9.99')


class FreeShippingStrategy(ShippingStrategy):
    def calculate(self, subtotal: Decimal) -> Decimal:
        return Decimal('0')


def get_shipping_strategy(strategy_name='standard'):
    strategy_name = (strategy_name or 'standard').strip().lower()
    strategies = {
        'standard': StandardShippingStrategy,
        'express': ExpressShippingStrategy,
        'free': FreeShippingStrategy,
    }
    strategy_class = strategies.get(strategy_name, StandardShippingStrategy)
    return strategy_class()


def calculate_shipping(subtotal, shipping_value=None, strategy_name='standard'):
    subtotal_decimal = Decimal(str(subtotal))
    if shipping_value is not None:
        try:
            shipping = Decimal(str(shipping_value))
        except (ArithmeticError, ValueError):
            shipping = get_shipping_strategy(strategy_name).calculate(subtotal_decimal)
    else:
        shipping = get_shipping_strategy(strategy_name).calculate(subtotal_decimal)

    if subtotal_decimal > Decimal('300'):
        return Decimal('0')
    return shipping
