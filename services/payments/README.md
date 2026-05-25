# payments service

The payments service is the heart of the platform. It accepts payment
authorisations, captures, voids, and refunds. Every state change is
recorded in the ledger service.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/payments` | Create and authorise a new payment |
| POST | `/payments/{id}/capture` | Capture a previously authorised payment |
| POST | `/payments/{id}/void` | Void an uncaptured authorisation |
| POST | `/payments/{id}/refund` | Refund a captured payment (full or partial) |
| GET | `/payments/{id}` | Fetch a payment by ID |

## State machine

```
        ┌───────────────┐
        │  authorised   │
        └───┬───────┬───┘
            │       │
       capture     void
            │       │
        ┌───▼───┐   │
        │ paid  │   │
        └───┬───┘   │
            │       │
         refund     │
            │       │
        ┌───▼───────▼───┐
        │   terminal    │
        └───────────────┘
```

A payment can only move forward. Refunds (full or partial) move a
captured payment into a terminal state — partial refunds may still be
followed by additional refunds until the captured amount is fully
returned, at which point the payment is fully refunded.

## Idempotency

All write endpoints accept an `Idempotency-Key` header. Repeated requests
with the same key return the original response — even days later — so
clients can retry safely on network errors.

## Dependencies

- `services/payments/main.py` — FastAPI app
- `services/payments/processor.py` — payment state machine
- `services/payments/gateways/` — external acquirer integrations (Stripe, Adyen)
