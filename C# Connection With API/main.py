from typing import Optional
import pyodbc as pyodbc
from fastapi import FastAPI, status, Response, HTTPException, Body, Depends
# from fastapi.params import Body
from fastapi.params import Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import oauth2
import Models

pass_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

#       Database Connection
try:
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-J04ALPE;"
        "Database=SampleStudent;"
        "Trusted_Connection=yes;"
    )
except Exception as error:
    print("Can't Connect to Database...")
    print("ERROR: ", error)

#   App Start Point. FASTAPI
app = FastAPI()


class StudentModel(BaseModel):
    StudentID: int
    Name: str
    Degree: str
    Hobbies: list


class UserModel(BaseModel):
    UserName: EmailStr
    Password: str


class GetUser(BaseModel):
    UserName: EmailStr
    Password: str


cursor = conn.cursor()


@app.post("/addstudent", status_code=status.HTTP_201_CREATED)
def addStudent(model: StudentModel, user: GetUser = Depends(oauth2.getCurrentUser)):
    print(user.UserName)
    hobbies = ", ".join(model.Hobbies)
    cursor.execute("INSERT INTO StudentInfo(ID, Name, Degree, hobbies) VALUES (?, ?, ?, ?)",
                   model.StudentID, model.Name, model.Degree, hobbies)
    cursor.commit()
    print(model)
    return model


@app.post("/createuser", status_code=status.HTTP_201_CREATED, response_model=Models.TokenModel)
def createuser(model: UserModel):
    model.Password = pass_context.hash(model.Password)
    cursor.execute("INSERT INTO Users(UserName, UserPassword) VALUES (?, ?)",
                   model.UserName, model.Password)
    cursor.commit()
    access_token = oauth2.createAccessToken(data={"UserName": model.UserName,
                                                  "Password": model.Password})
    return {"access_token": access_token, "type": "bearer"}


# @app.get("/getuser/{username}&{userpass}", status_code=status.HTTP_302_FOUND, response_model=GetUser)
# def getUser(username, userpass):
#     cursor.execute("select * from Users where UserName = ?", username)
#     rows = cursor.fetchone()
#     if rows is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User Name or Password")
#     else:
#         result = {}
#         if pass_context.verify(userpass, rows[2]):
#             access_token = oauth2.createAccessToken(data={"UserName": username,
#                                            "Password": userpass})
#             # result = {"UserName": rows[1],
#             #           "Password": rows[2]}
#             return {"access_token": access_token, "token_type": "bearer"}
#         else:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User Name or Password")

@app.post("/login", response_model=Models.TokenModel)
def login(user: GetUser):
    cursor.execute("select * from Users where UserName = ?", user.UserName)
    rows = cursor.fetchone()
    if rows is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User Name or Password")
    else:
        result = {}
        if pass_context.verify(user.Password, rows[2]):
            access_token = oauth2.createAccessToken(data={"UserName": user.UserName,
                                                          "Password": user.Password})
            # result = {"UserName": rows[1],
            #           "Password": rows[2]}
            return {"access_token": access_token, "type": "Bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid User Name or Password")


@app.get("/getstudents", status_code=status.HTTP_200_OK)
def getStudents(user: GetUser = Depends(oauth2.getCurrentUser)):
    print(user.UserName)
    model: StudentModel
    cursor.execute("SELECT * FROM StudentInfo")
    data = cursor.fetchall()
    result = {}
    details = []
    for rows in data:
        result = {"StudentID": rows[0],
                  "Name": rows[1],
                  "Degree": rows[2],
                  "Hobbies": str(rows[3]).split(", ")
                  }
        details.append(result)
    return {"StudentData": details}
