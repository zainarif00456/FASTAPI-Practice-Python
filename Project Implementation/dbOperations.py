import datetime

import pyodbc
import models

#       Database Connection
try:
    conn = pyodbc.connect(
        "Driver={SQL Server Native Client 11.0};"
        "Server=DESKTOP-J04ALPE;"
        "Database=GCS;"
        "Trusted_Connection=yes;"
    )
except Exception as error:
    print("Can't Connect to Database...")
    print("ERROR: ", error)


def createAccount(model: models.SignUp):
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO AdminPanel(UserName, EmailAddress, Gender, DateOfBirth, UserPassword, ActiveStatus) values"
            "(?, ?, ?, ?, ?, ?)", model.UserName, model.EmailAddress, model.Gender, model.DateOfBirth,
            model.UserPassword, model.ActiveStatus)
        cursor.commit()
        print("ENTRY SUCCESS")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def loginAccount(model: models.Login):
    cursor = conn.cursor()
    try:
        cursor.execute("select * from AdminPanel where UserName = ?", model.UserName)
        row = cursor.fetchone()
        user = models.SignUp
        user.ID = row[0]
        user.UserName = row[1]
        user.EmailAddress = row[2]
        user.Gender = row[3]
        user.DateOfBirth = row[4]
        user.UserPassword = row[5]
        user.ActiveStatus = row[6]
        return user

    except Exception as e:
        print(f"Error: {e}")
        return None


def addEmployee(model: models.Employee):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employee(FullName, "
                   "CNIC,"
                   "Gender,"
                   "EmailAddress,"
                   "PhoneNo,"
                   "DateOfBirth,"
                   "Department,"
                   "AddedBy,"
                   "EntryTime) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", model.FullName, model.CNIC, model.Gender,
                   model.EmailAddress,
                   model.PhoneNo, model.DateOfBirth, model.Department, model.AddedBy, datetime.datetime.utcnow())
    cursor.commit()


def getEmployees():
    cursor = conn.cursor()
    cursor.execute("select * from Employee")
    data = cursor.fetchall()
    if data is None:
        return None
    details = {}
    result = []
    for rows in data:
        details = {
            "ID": rows[0],
            "FullName": rows[1],
            "CNIC": rows[2],
            "Gender": rows[3],
            "EmailAddress": rows[4],
            "PhoneNo": rows[5],
            "DateOfBirth": rows[6],
            "Department": rows[7],
            "AddedBy": rows[8],
            "EntryTime": rows[9]
        }
        result.append(details)
    return {"EmployeeInformation": result}


def getEmployeeByID(id: int):
    cursor = conn.cursor()
    cursor.execute("select * from Employee where ID=?", id)
    rows = cursor.fetchone()
    if rows is None:
        return None
    details = {
        "ID": rows[0],
        "FullName": rows[1],
        "CNIC": rows[2],
        "Gender": rows[3],
        "EmailAddress": rows[4],
        "PhoneNo": rows[5],
        "DateOfBirth": rows[6],
        "Department": rows[7],
        "AddedBy": rows[8],
        "EntryTime": rows[9]
    }
    return details


def updateEmployee(id, model: models.Employee):
    cursor = conn.cursor()
    try:
        cursor.execute("update Employee set FullName=?, CNIC=?, Gender=?, EmailAddress=?, PhoneNo=?,"
                       "DateOfBirth=?, Department=?, AddedBy=?, EntryTime=? where ID=?", model.FullName, model.CNIC,
                       model.Gender, model.EmailAddress, model.PhoneNo, model.DateOfBirth, model.Department,
                       model.AddedBy,
                       datetime.datetime.now(), id)
        cursor.commit()
        return True
    except Exception as e:
        return False


def deleteEmployee(id):
    cursor = conn.cursor()
    try:
        cursor.execute("delete from Employee where ID = ?", id)
        return True
    except:
        return False
