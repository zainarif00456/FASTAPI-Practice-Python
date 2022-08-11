from typing import Optional
import DBOperations as db
import pyodbc as pyodbc
from fastapi import FastAPI, status, Response, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel


#       Database Connection
try:
    conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-J04ALPE;"
            "Database=STUDENTS;"
            "Trusted_Connection=yes;"
        )
except Exception as error:
    print("Can't Connect to Database...")
    print("ERROR: ", error)

#   App Start Point. FASTAPI
app = FastAPI()



@app.get("/")
def root():
    students = db.getAllStudents()
    return students



