from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette import status
import models
from fastapi.security import OAuth2PasswordBearer

oth2scheme = OAuth2PasswordBearer(tokenUrl='login')

"""
Things Needed:
1- SECRET KEY
2- Algorithm
3- Expiration TIme
"""

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def createAccessToken(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_accrss_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("ID")
        username: str = payload.get("UserName")
        password: str = payload.get("UserPassword")
        token_data = models.TokenData(ID=id, UserName=username, Password=password)
    except JWTError as e:
        raise credentials_exception
    return token_data


def getCurrentUser(token: str = Depends(oth2scheme)):
    cred = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could Not Validate Credentials",
                         headers={"WWW-Authenticate": "Bearer"})
    data = verify_accrss_token(token, cred)
    return data

