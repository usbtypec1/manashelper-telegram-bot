from uuid import UUID

from pydantic import BaseModel


class Faculty(BaseModel):
    id: UUID
    name: str
