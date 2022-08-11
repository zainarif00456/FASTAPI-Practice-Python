from typing import Optional
from fastapi import FastAPI, status, Response, HTTPException, Body, Depends
from fastapi.params import Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import authentication
import models
import dbOperations as db
pass_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


app = FastAPI()

@app.post("/signup")
def signup(model: models.SignUp):
    model.UserPassword = pass_context.hash(model.UserPassword)
    if db.createAccount(model):
        return {"Admin": "Account Successfully Created"}
        pass
    else:
        print("Error Occured")
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail={"Details": "ERROR OCCURED"})


@app.post("/login")
def login(model: models.Login):
    user: models.SignUp
    user = db.loginAccount(model)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
       if pass_context.verify(model.Password, user.UserPassword):
           data = {"UserName": user.UserName,
                   "UserPassword": user.UserPassword}
           access_token = authentication.createAccessToken(data)
           return {"access_token": access_token, "type": "Bearer"}
       else:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"Information": "Authorized User OR Invalid Credentials"})

