from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserSchema(BaseModel):
    """
    Schema for user registration data.
    """

    username: str = Field(min_length=5, max_length=25)
    email: EmailStr
    password: str = Field(min_length=6, max_length=30)

    model_config = ConfigDict(
        json_schema_extra={
            "title": "User Schema",
            "description": "Schema for user registration data",
            "example": {
                "username": "sergiokapone",
                "email": "example@example.com",
                "password": "qwer1234",
            },
        }
    )
