from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ShippingQuote:
    service: str
    price: Decimal
    business_days: int


class SimulatedShippingService:
    """Substituir por um adaptador real quando houver credenciais de transportadora."""

    def quote(self, zip_code: str, subtotal: Decimal) -> ShippingQuote:
        if subtotal >= Decimal("399.00"):
            return ShippingQuote("Frete grátis", Decimal("0.00"), 7)
        suffix = int("".join(filter(str.isdigit, zip_code))[-1:] or 0)
        return ShippingQuote("Entrega padrão", Decimal("19.90") + Decimal(suffix), 6 + suffix % 4)

