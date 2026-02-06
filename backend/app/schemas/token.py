from pydantic import BaseModel

class Token(BaseModel):
    email: str | None = None
    access_token: str
    token_type: str
