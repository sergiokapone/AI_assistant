from pydantic import BaseModel, Field

class Response(BaseModel):
    string: str = Field()