from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    UserName: EmailStr
    Password: str

class TokenModel(BaseModel):
    access_token: str
    type: str