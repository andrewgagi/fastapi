from fastapi import FastAPI, Depends, HTTPException, Response, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id:{id} not found"
    )


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id:{id} not found"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    update_post = post_query.first()
    if not update_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id:{id} not found"
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"Updated", post_query.first()}


# while True:
#     try:
#         connection = psycopg2.connect(
#             user="postgres",
#             password="Happy2023.",
#             host="localhost",
#             port="5432",
#             database="fastapi",
#             cursor_factory=RealDictCursor,
#         )
#         cursor = connection.cursor()
#         # print(connection.get_dsn_parameters(), "\n")
#         break
#     except (Exception, psycopg2.Error) as error:
#         print("Error while connecting to PostgreSQL", error)
#         time.sleep(2)
#         # Print PostgreSQL Connection properties


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = False


# @app.get("/")
# async def root():
#     return {"message": "Hello World."}


# @app.get("/posts")
# def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     my_post = cursor.fetchall()
#     return my_post


# @app.get("/posts/{id}", status_code=status.HTTP_200_OK)
# def get_post(id: int):
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))

#     my_post = cursor.fetchone()
#     # print(my_post)
#     if my_post:
#         return my_post
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute(
#         """INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
#         (post.title, post.content, post.published),
#     )
#     connection.commit()
#     my_post = cursor.fetchone()

#     return {"data_recieved": my_post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
#     my_post = cursor.fetchone()
#     connection.commit()
#     if my_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id:{id} not found"
#         )
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
# def update_post(id: int, post: Post):
#     cursor.execute(
#         """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#         (post.title, post.content, post.published, id),
#     )
#     connection.commit()
#     my_post = cursor.fetchone()
#     if my_post == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"Post id:{id} not found"
#         )
#     return my_post
