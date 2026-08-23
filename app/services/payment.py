from dataclasses import dataclass
from uuid import uuid4


@dataclass
class PaymentResult:
    approved: bool
    reference: str
    status: str


class SimulatedPaymentGateway:
    """Não recebe nem persiste dados sensíveis de cartão."""

    ALLOWED_METHODS = {"pix", "credito", "debito", "boleto", "apple_pay"}

    def charge(self, method: str) -> PaymentResult:
        if method not in self.ALLOWED_METHODS:
            return PaymentResult(False, f"SIM-{uuid4().hex[:12].upper()}", "recusado")
        return PaymentResult(True, f"SIM-{uuid4().hex[:12].upper()}", "aprovado")

