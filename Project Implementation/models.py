from pydantic import BaseModel, EmailStr
from datetime import datetime

class SignUp(BaseModel):
    UserName: str
    EmailAddress: EmailStr
    Gender: str
    DateOfBirth: str
    UserPassword: str
    ActiveStatus: str = "$"

class Login(BaseModel):
    UserName: str
    Password: str


class TokenData(BaseModel):
    UserName: EmailStr
    Password: str

class TokenModel(BaseModel):
    access_token: str
    type: str