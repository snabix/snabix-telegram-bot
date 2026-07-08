# Стратегия тестирования Telegram-бота

## Проверки

```bash
cd /Users/dustun/Projects/snabix/snabix-telegram-bot
task check
```

Без `go-task` команды можно запустить напрямую:

```bash
PYTHONPATH=src .venv/bin/ruff check .
PYTHONPATH=src .venv/bin/mypy src tests
PYTHONPATH=src .venv/bin/pytest
```

## Что тестировать

- parsing настроек;
- admin access;
- backend client;
- DTO validation;
- common handlers;
- admin handlers;
- callback handlers;
- ошибки backend API.

## Ручной smoke

После изменений проверь в Telegram:

- `/start`;
- `/help`;
- `/health`;
- `/me`;
- `/stats`;
- inline-кнопку обновления;
- кнопку открытия admin panel;
- запрет admin-команд для неадмина.

## Правила

- Не мокать всё приложение целиком, если можно проверить конкретный handler/service.
- Не обращаться к реальному production backend в тестах.
- Не печатать секреты в test output.
- Для новых backend endpoints добавлять DTO и тест клиента.
