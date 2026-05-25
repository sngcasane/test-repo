# auth service

The auth service issues and validates JWTs, manages user sessions in
Redis, and is the single source of truth for "who is this request from."

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/login` | Email + password → access token + refresh token |
| POST | `/refresh` | Exchange a refresh token for a new access token |
| POST | `/logout` | Invalidate the current session |
| GET | `/me` | Return the authenticated user's profile |

## Token strategy

- **Access tokens** — JWT, 15 minute TTL, signed with HS256. Carry the
  user ID, the role, and the session ID. Never persisted server-side.
- **Refresh tokens** — opaque random strings, 30 day TTL. Stored in
  Redis keyed by session ID. Rotated on every use (refresh token reuse
  detection).

## Database

Owns the `auth` schema. Tables:

- `users` — user identity (email, hashed password, role, created_at)
- `password_reset_tokens` — one-time-use reset tokens

Sessions live in Redis, not Postgres. Session data is ephemeral.

## Dependencies

- `services/auth/main.py` — FastAPI app + lifespan
- `services/auth/routes.py` — endpoint handlers
- `services/auth/tokens.py` — JWT issuance, refresh rotation
