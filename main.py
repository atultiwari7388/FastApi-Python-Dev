from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

#create instance
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_Posts():
    return {"data":"This is Your Posts"}


@app.post("/createPosts")
def create_Posts(post: Post):
    print(post.dict())
    print(post)
    return {"data": post.dict()}