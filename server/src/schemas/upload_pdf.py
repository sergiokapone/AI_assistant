from typing import Any
from pydantic import BaseModel, Field, EmailStr


class UploadSchema(BaseModel):
    name: str
    string: Field(...)
    description: str
    upload: Any

