from typing import Any
from pydantic import BaseModel


class UploadSchema(BaseModel):
    upload: Any

