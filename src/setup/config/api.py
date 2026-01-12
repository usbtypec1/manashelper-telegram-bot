from pydantic import BaseModel

from repositories.http_client import ApiBaseUrl


class ApiSettings(BaseModel):
    base_url: ApiBaseUrl
