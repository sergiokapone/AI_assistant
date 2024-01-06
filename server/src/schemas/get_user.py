from pydantic import BaseModel, Field


class Message_History(BaseModel):
    history: list