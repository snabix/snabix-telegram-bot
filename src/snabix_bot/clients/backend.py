from dataclasses import dataclass
from typing import Any, Optional

import aiohttp


@dataclass(frozen=True)
class BackendHealth:
    ok: bool
    status: int
    message: str


class BackendClient:
    def __init__(self, base_url: str, service_token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._service_token = service_token

    async def health(self) -> BackendHealth:
        try:
            data = await self._request("GET", "/health")
        except aiohttp.ClientResponseError as exc:
            return BackendHealth(ok=False, status=exc.status, message=exc.message)
        except aiohttp.ClientError as exc:
            return BackendHealth(ok=False, status=0, message=str(exc))

        return BackendHealth(
            ok=True,
            status=200,
            message=str(data.get("message", "Backend is available.")),
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self._service_token}",
        }

        async with (
            aiohttp.ClientSession(headers=headers) as session,
            session.request(method, f"{self._base_url}{path}", json=json) as response,
        ):
            response.raise_for_status()
            payload = await response.json(content_type=None)

        return payload if isinstance(payload, dict) else {"data": payload}
