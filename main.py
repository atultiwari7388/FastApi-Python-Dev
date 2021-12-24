from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

#create instance
app = FastAPI()

#pydantic schema
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#hard code example
my_posts = [{"title":"title of post 1", "content":"content of post 1", "published":True, "rating":5, "id":1},{"title":"title of post 2", "content":"content of post 2", "published":True, "rating":5, "id":2},{"title":"title of post 3", "content":"content of post 3", "published":True, "rating":5, "id":3} ]

#find post func
def find_posts(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


#find index posts
def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i
    return None

#root directory
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_Posts():
    return {"data": my_posts}

#create post method
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_Posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post.dict()}

#find post by id
@app.get("/posts/{id}")
def get_Post(id:int, response: Response):
    print(id)
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post not found with id:{id}"}
    return {"post_details": post}

#delete the posts

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_Post(id:int, response: Response):
    #find the index in the array that has required id
    index = find_index_post(id)

    my_posts.pop(index)
    return {"message": f"Post with id:{id} deleted"}


#upadted the posts

@app.put("/posts/{id}")
def update_Post(id:int, post:Post, response: Response):
    index = find_index_post(id)
    if index ==  None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Post not found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"message": post_dict}
