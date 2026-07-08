# Секреты Telegram-бота

## Что нельзя коммитить

- `SNABIX_BOT_TOKEN`;
- `SNABIX_BACKEND_SERVICE_TOKEN`;
- `SNABIX_BOT_WEBHOOK_SECRET`;
- реальные Telegram admin ids без необходимости;
- `.env`.

## Основной env

```text
$PROJECT_ROOT/snabix-telegram-bot/.env
```

Пример:

```text
$PROJECT_ROOT/snabix-telegram-bot/.env.example
```

## Переменные

```env
SNABIX_BOT_TOKEN=
SNABIX_BACKEND_SERVICE_TOKEN=
SNABIX_BOT_WEBHOOK_SECRET=
SNABIX_ADMIN_TELEGRAM_IDS=
```

## Генерация webhook secret

```bash
openssl rand -hex 32
```

## Ротация bot token

1. Создать новый token в BotFather.
2. Обновить `.env`.
3. Перезапустить bot.
4. Проверить `/start`.

## Ротация backend service token

1. Сгенерировать новый token.
2. Обновить backend `SNABIX_BOT_SERVICE_TOKEN`.
3. Обновить bot `SNABIX_BACKEND_SERVICE_TOKEN`.
4. Перезапустить backend и bot.
5. Проверить `/health`.
