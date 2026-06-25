from typing import Any, Optional

import aiohttp

from snabix_bot.schemas.backend import BackendHealthDto


class BackendClient:
    def __init__(self, base_url: str, service_token: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._service_token = service_token
        self._session: Optional[aiohttp.ClientSession] = None

    async def health(self) -> BackendHealthDto:
        try:
            data = await self._request("GET", "/health")
        except aiohttp.ClientResponseError as exc:
            return BackendHealthDto(ok=False, status=exc.status, message=exc.message)
        except aiohttp.ClientError as exc:
            return BackendHealthDto(ok=False, status=0, message=str(exc))

        return BackendHealthDto.model_validate(data)

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self._service_token}",
            })

        return self._session

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        session = await self._get_session()

        async with session.request(method, f"{self._base_url}{path}", json=json) as response:
            response.raise_for_status()
            payload = await response.json(content_type=None)

        return payload if isinstance(payload, dict) else {"data": payload}
