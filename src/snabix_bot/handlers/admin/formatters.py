from snabix_bot.schemas.backend import (
    BackendHealthDto,
    BackendServiceIdentityDto,
    BackendStatsDto,
)


def format_health(result: BackendHealthDto) -> str:
    status = "Доступен" if result.ok else "Недоступен"

    return f"Backend health\n\nСтатус: {status}\nHTTP: {result.status}\nСообщение: {result.message}"


def format_identity(identity: BackendServiceIdentityDto) -> str:
    return (
        "Service API\n\n"
        "Подключение: активно\n"
        f"Сервис: {identity.service}\n"
        f"Режим: {identity.mode}\n"
        f"Версия: {identity.version}"
    )


def format_stats(summary: BackendStatsDto) -> str:
    return (
        "Статистика Snabix\n\n"
        f"Пользователи: {summary.users_total}\n"
        f"Объявления всего: {summary.listings_total}\n"
        f"На модерации: {summary.listings_pending_review}\n"
        f"Опубликовано: {summary.listings_published}\n"
        f"В архиве: {summary.listings_archived}"
    )
