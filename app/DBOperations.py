import pyodbc

"""
Contains the function for database operations
"""



try:
    conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-J04ALPE;"
            "Database=STUDENTS;"
            "Trusted_Connection=yes;"
        )
    cursor = conn.cursor()
except Exception as error:
    print("Can't Connect to Database...")
    print("ERROR: ", error)


def getAllStudents():
    cursor.execute("select * from StudentInformation")
    students = {}
    for row in cursor.fetchall():
        students[row[0]] = {
            "Name of Student": row[1],
            "Gender": row[2],
            "Father's Name": row[3],
            "Father's Phone No": row[4],
            "Father's CNIC": row[5],
            "Home Address": row[6],
            "Class Enrolled": row[7],
            "Date of Birth": row[8],
            "In Case of Emergency": {
                "Name": row[9],
                "Phone No": row[10]
            },
            "Profile Picture": row[11]
        }
    return students




# if __name__ == '__main__':
#     getAllStudents()
