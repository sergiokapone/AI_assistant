from pydantic import BaseModel, Field


class UploadPDFSchema(BaseModel):
    string: str = Field()