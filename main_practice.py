import datetime
from typing import Optional

import pyodbc as pyodbc
from fastapi import FastAPI, status, Response, HTTPException
# from fastapi.params import Body
from pydantic import BaseModel


#       Database Connection
try:
    conn = pyodbc.connect(
            "Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-J04ALPE;"
            "Database=FASTAPI;"
            "Trusted_Connection=yes;"
        )
    cursor = conn.cursor()
except Exception as error:
    print("Can't Connect to Database...")
    print("ERROR: ", error)



app = FastAPI()

#   Global Declarations

my_posts = [{"title": "Sample Post", "content": "Sample Content", "published": True}]


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


@app.get("/")
def read_root():
    return {"Name": "Zain Ul Abdeen"}

@app.get("/students")
def get_Students():
    return {"Name": "Zain Ul Abdeen",
            "Program": "BS Computer Science",
            "University": "Superior University Lahore",
            "Campus Name": "Superior University Gold Campus",
            "Email Address": "zainarif00456@gmail.com",
            "Skills": ["Python", "C++", "C#", "ASP.NET MVC", "Java", "HTML", "CSS", "MSSQL Database"]
            }


@app.get("/posts")
def get_posts():
    post: Post
    cursor.execute("""SELECT * FROM Posts""")
    posts = cursor.fetchall()
    result = {}
    for rows in posts:
        result[rows[0]] = {
            "title": rows[1],
            "content": rows[2],
            "Time of Upload": rows[3]
        }
    return result


@app.post("/create", status_code=status.HTTP_201_CREATED)
def createPost(post: Post):
    cursor.execute("""INSERT INTO Posts(Title, Content, DateOfUpload)
    values(?, ?, ?)""", post.title, post.content, datetime.datetime.now())
    cursor.commit()
    return {"data": post}

    # print(post)
    # my_posts.append(post.dict())
    # return {"new_post": f"title: {post.title}, content: {post.content}"}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"data": f"No Post Found by ID = {id}"}
    result = {}
    cursor.execute("""Select * from Posts where ID = ?""", id)
    rows = cursor.fetchone()
    if rows is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Post Found by ID = {id}")
    result[rows[0]] = {
        "title": rows[1],
        "content": rows[2],
        "Time of Upload": rows[3]
    }
    return result



@app.delete("/deleteposts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM Posts where ID = ?", id)


@app.put("/update/{id}")
def update_post(id: int, post: Post):
    cursor.execute("UPDATE Posts set Title = ?, Content = ? where ID = ?", post.title, post.content, id)
    cursor.commit()
    return {"data": f"Updated Successfully at {datetime.datetime.now()}"}



