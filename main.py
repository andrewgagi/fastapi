from typing import Optional
from fastapi import Body, FastAPI
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



@app.post("/posts")
def create_post(new_post: Post):
    post = new_post.dict()
    post["id"] = randint(100, 99999)
    my_post.append(post)
    return {"data_recieved": my_post}
