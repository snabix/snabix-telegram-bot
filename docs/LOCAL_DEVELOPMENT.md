# Локальная разработка Telegram-бота

## Первый запуск

```bash
cd $PROJECT_ROOT/snabix-telegram-bot
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
PYTHONPATH=src .venv/bin/python -m snabix_bot
```

Если установлен `go-task`, можно короче:

```bash
task setup
task run
```

## Обязательные переменные

```env
SNABIX_BOT_TOKEN=replace-with-bot-token
SNABIX_BOT_MODE=polling
SNABIX_BACKEND_BASE_URL=http://127.0.0.1:8080/api/v1
SNABIX_BACKEND_SERVICE_TOKEN=replace-with-backend-service-token
SNABIX_ADMIN_PANEL_URL=http://127.0.0.1:8080/admin
SNABIX_ADMIN_TELEGRAM_IDS=123456789
```

`SNABIX_BACKEND_SERVICE_TOKEN` должен совпадать с backend `SNABIX_BOT_SERVICE_TOKEN`.

## Polling режим

Рекомендуется для локальной разработки:

```bash
PYTHONPATH=src .venv/bin/python -m snabix_bot
```

## Webhook режим

Запусти HTTPS tunnel:

```bash
ngrok http 9000
```

Настрой `.env`:

```env
SNABIX_BOT_MODE=webhook
SNABIX_BOT_WEBHOOK_URL=https://your-ngrok-domain.ngrok-free.app/webhook/telegram
SNABIX_BOT_WEBHOOK_PATH=/webhook/telegram
SNABIX_BOT_WEBHOOK_SECRET=generated-secret
SNABIX_BOT_HOST=0.0.0.0
SNABIX_BOT_PORT=9000
```

Запусти:

```bash
PYTHONPATH=src .venv/bin/python -m snabix_bot
```

## Частые проблемы

### Порт 9000 занят

Проверь процесс:

```bash
lsof -i :9000
```

Можно временно поменять:

```env
SNABIX_BOT_PORT=9001
```

### Backend-сервис недоступен

Проверь:

- backend запущен;
- `SNABIX_BACKEND_BASE_URL`;
- service token совпадает;
- endpoint `/api/v1/service/bot/health`.

### Команды не отображаются в Telegram

Бот регистрирует команды при запуске. Перезапусти bot и обнови Telegram client.

## Проверки

```bash
task check
```
