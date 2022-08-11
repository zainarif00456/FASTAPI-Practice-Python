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
        cursor.execute("INSERT INTO AdminPanel(UserName, EmailAddress, Gender, DateOfBirth, UserPassword, ActiveStatus) values"
                       "(?, ?, ?, ?, ?, ?)", model.UserName, model.EmailAddress, model.Gender, model.DateOfBirth, model.UserPassword, model.ActiveStatus)
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


#   App Start Point. FASTAPI
