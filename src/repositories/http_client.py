from collections.abc import AsyncGenerator
from typing import NewType

import httpx
from pydantic import HttpUrl


ApiBaseUrl = NewType("ApiBaseUrl", HttpUrl)
ApiHttpClient = NewType("ApiHttpClient", httpx.AsyncClient)


async def get_api_http_client(
    base_url: ApiBaseUrl,
) -> AsyncGenerator[ApiHttpClient, None]:
    async with httpx.AsyncClient(
        base_url=str(base_url),
    ) as http_client:
        yield ApiHttpClient(http_client)
