# Чеклист релиза Telegram-бота

## Автоматические проверки

```bash
task check
```

## Env

Проверь:

- `SNABIX_BOT_TOKEN`;
- `SNABIX_BOT_MODE`;
- `SNABIX_BACKEND_BASE_URL`;
- `SNABIX_BACKEND_SERVICE_TOKEN`;
- `SNABIX_ADMIN_TELEGRAM_IDS`;
- webhook-настройки, если используется webhook.

Production env должен пройти проверку на placeholder secrets:

```bash
PRODUCTION_ENV_FILE=/path/to/.env.production task secrets:production
```

Запрещено деплоить значения из `.env.example`, включая `replace-with-bot-token`, `replace-with-backend-service-token` и `replace-with-random-webhook-secret`. Если placeholder попал в staging или production, выполни ротацию bot token, backend service token или webhook secret и проверь access logs.

## Совместимость с backend-сервисом

Перед релизом bot проверь, что backend поддерживает:

- `/api/v1/service/bot/health`;
- `/api/v1/service/bot/me`;
- `/api/v1/service/bot/stats`;
- актуальный bearer-token.

## Ручной smoke

- Бот запускается.
- Команды отображаются в Telegram.
- `/health` отвечает.
- `/me` отвечает.
- `/stats` отвечает.
- Неадмин не получает доступ к admin-командам.

## Перед push

```bash
git status --short
git diff --check
```

Рекомендуемое сообщение:

```text
docs(): add bot handbook
```
