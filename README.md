# Snabix Bot

Telegram service bot for Snabix.

The first version is intentionally admin/service-oriented:

- admin health checks;
- important backend notifications;
- moderation shortcuts;
- future user notification delivery after Telegram account linking.

## Architecture

The bot is a separate Python service. It does not connect to the database directly.

```text
Telegram <-> snabix-bot <-> Snabix Backend API <-> database
```

Backend remains the source of truth for users, roles, listings, notifications and permissions.
The bot should call service endpoints with `SNABIX_BACKEND_SERVICE_TOKEN`.

## Local Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
python -m snabix_bot
```

Do not commit `.env`.

## Suggested MVP

1. `/start` and `/help` for basic bot onboarding.
2. `/health` for admin-only backend availability checks.
3. Admin channel notifications for important events.
4. Moderation actions through buttons that call backend API.
5. User Telegram linking flow later, after backend support is ready.
