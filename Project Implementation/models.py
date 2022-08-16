from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class SignUp(BaseModel):
    ID: Optional[int]
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
    ID: int
    UserName: str
    Password: str


class TokenModel(BaseModel):
    access_token: str
    type: str


class Employee(BaseModel):
    FullName: str
    CNIC: str
    Gender: str
    EmailAddress: EmailStr
    PhoneNo: str
    DateOfBirth: datetime
    Department: str
    AddedBy: int


class AdminModel(BaseModel):
    ID: int
    UserName: str
    Password: str
