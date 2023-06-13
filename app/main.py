from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from random import randint

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None


my_post = [
    {"id": 1, "title": "Hello World", "content": "This is my first post."},
    {"id": 2, "title": "FastAPI", "content": "This is my second post."},
]


@app.get("/")
async def root():
    return {"message": "Hello World."}


@app.get("/posts")
def get_posts():
    return my_post

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for post in my_post:
        if post["id"] == post_id:
            return post
    if post_id not in my_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post = new_post.dict()
    post["id"] = randint(100, 99999)
    my_post.append(post)
    return {"data_recieved": my_post}

@app.delete("/posts/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for post in my_post:
        if post["id"] == post_id:
            my_post.remove(post)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

@app.put("/posts/{post_id}",status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id: int, post: Post):
    for p in my_post:
        if p["id"] == post_id:
            p["title"] = post.title
            p["content"] = post.content
            p["published"] = post.published
            p["rating"] = post.rating
            return {"message": "Post has been updated successfully!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
