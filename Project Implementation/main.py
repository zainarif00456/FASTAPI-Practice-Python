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
        print("Error Occurred")
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail={"Details": "ERROR OCCURRED"})


@app.post("/login")
def login(model: models.Login):
    user: models.SignUp
    user = db.loginAccount(model)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        if pass_context.verify(model.Password, user.UserPassword):
            data = {"ID": user.ID,
                    "UserName": user.UserName,
                    "UserPassword": user.UserPassword}
            access_token = authentication.createAccessToken(data)
            return {"access_token": f"Bearer {access_token}"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail={"Information": "Unauthorized User OR Invalid Credentials"})


@app.post("/employees", status_code=status.HTTP_201_CREATED)
def employees(model: models.Employee, admin: models.AdminModel = Depends(authentication.getCurrentUser)):
    model.AddedBy = admin.ID
    db.addEmployee(model)
    return {"Details": "Employee Added Successfully"}


@app.get("/getemployees", status_code=status.HTTP_200_OK)
def employees(admin: models.AdminModel = Depends(authentication.getCurrentUser)):
    data = db.getEmployees()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"details": "Employees Not Found"})
    else:
        return data


@app.get("/getemployeebyid/{id}", status_code=status.HTTP_200_OK)
def employees(id: int, admin: models.AdminModel = Depends(authentication.getCurrentUser)):
    data = db.getEmployeeByID(id)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"details": "Employees Not Found"})
    else:
        return data


@app.post("/updateemployee/{id}", status_code=status.HTTP_200_OK)
def update(id: int, model: models.Employee, admin: models.AdminModel = Depends(authentication.getCurrentUser)):
    model.AddedBy = admin.ID
    flag = db.updateEmployee(id, model)
    if flag:
        return {"detail": "Employee Updated Successfully..."}
    else:
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail={"details": "Can't Update Employee..."})

@app.delete("/deleteemployee/{id}")
def delete(id: int, admin:models.AdminModel=Depends(authentication.getCurrentUser)):
    flag = db.deleteEmployee(id)
    if flag:
        return {"detail": "Employee Updated Successfully..."}
    else:
        raise HTTPException(status_code=status.WS_1011_INTERNAL_ERROR, detail={"details": "Can't Delete Employee..."})