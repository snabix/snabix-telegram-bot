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

Значения из `.env.example` предназначены только для локального запуска и документации формы env. Их нельзя переносить в staging или production.

## Переменные

```env
SNABIX_BOT_TOKEN=
SNABIX_BACKEND_SERVICE_TOKEN=
SNABIX_BOT_WEBHOOK_SECRET=
SNABIX_ADMIN_TELEGRAM_IDS=
```

## Запрещенные значения для staging и production

Production env не должен содержать placeholder values:

```text
SNABIX_BOT_TOKEN=replace-with-bot-token
SNABIX_BACKEND_SERVICE_TOKEN=replace-with-backend-service-token
SNABIX_BACKEND_SERVICE_TOKEN=change-me
SNABIX_BOT_WEBHOOK_SECRET=replace-with-random-webhook-secret
```

Перед деплоем запусти guard против реального env-файла:

```bash
PRODUCTION_ENV_FILE=/path/to/.env.production task secrets:production
```

CI запускает self-test guard:

```bash
python scripts/check_production_secrets.py --self-test
```

Для staging и production нужны отдельные значения:

- `SNABIX_BOT_TOKEN`: реальный token из BotFather для конкретного окружения;
- `SNABIX_BACKEND_SERVICE_TOKEN`: тот же сгенерированный service token, что и backend `SNABIX_BOT_SERVICE_TOKEN`;
- `SNABIX_BOT_WEBHOOK_SECRET`: отдельный webhook secret минимум 32 случайных символа;
- `SNABIX_ADMIN_TELEGRAM_IDS`: только реальные администраторы окружения.

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

Если placeholder или dev token попал в staging/production, сразу выполни ротацию: сгенерируй новый token, обнови secret-хранилище, перезапусти backend и bot, проверь `/health` и access logs.
