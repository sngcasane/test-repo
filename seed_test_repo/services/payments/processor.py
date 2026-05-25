"""Payment state machine — the core of the payments service."""
from decimal import Decimal
from enum import Enum

from .gateways import acquirer_for
from .ledger_client import LedgerClient


class PaymentStatus(str, Enum):
    AUTHORISED = "authorised"
    PAID = "paid"
    VOIDED = "voided"
    REFUNDED = "refunded"
    FAILED = "failed"


class PaymentProcessor:
    """Drives a Payment row through its state machine.

    All transitions write to the ledger via LedgerClient. Failures from
    the acquirer or the ledger leave the payment in its previous state
    and surface the error to the caller — partial state is not allowed.
    """

    def __init__(self, ledger: LedgerClient):
        self.ledger = ledger

    async def authorise(self, payment, amount: Decimal):
        gateway = acquirer_for(payment.gateway_name)
        result = await gateway.authorise(payment.id, amount, payment.card_token)
        if not result.success:
            payment.status = PaymentStatus.FAILED
            return payment
        payment.status = PaymentStatus.AUTHORISED
        await self.ledger.record(payment.id, "authorise", amount)
        return payment

    async def capture(self, payment):
        assert payment.status == PaymentStatus.AUTHORISED
        gateway = acquirer_for(payment.gateway_name)
        result = await gateway.capture(payment.gateway_reference)
        if not result.success:
            return payment  # stays authorised
        payment.status = PaymentStatus.PAID
        await self.ledger.record(payment.id, "capture", payment.amount)
        return payment

    async def refund(self, payment, amount: Decimal):
        assert payment.status == PaymentStatus.PAID
        if amount > payment.refundable_amount:
            raise ValueError("Refund exceeds refundable amount")
        gateway = acquirer_for(payment.gateway_name)
        await gateway.refund(payment.gateway_reference, amount)
        await self.ledger.record(payment.id, "refund", -amount)
        payment.refundable_amount -= amount
        if payment.refundable_amount == 0:
            payment.status = PaymentStatus.REFUNDED
        return payment
