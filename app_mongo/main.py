from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from pydantic import BaseModel
from typing import Optional, Text, List
from datetime import datetime
import motor.motor_asyncio

app = FastAPI()
# db connection
client = motor.motor_asyncio.AsyncIOMotorClient('192.168.1.50')
db = client.fastapiblog


@app.get("/")
def read_root():
    return {"message": "Welcome to my very Basic FastAPI!"}


# post model
class Post(BaseModel):
    id: int
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()

    # https://www.mongodb.com/developer/quickstart/python-quickstart-fastapi/
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "id": "1",
                "title": "Getting started with FastAPI",
                "author": "Anish Sebastian",
                "content": "Hello FastAPI!",
                "created_at": datetime.utcnow()
            }
        }


# route to view all posts.
@app.get("/blog", response_description="List all posts", response_model=List[Post])
async def get_posts():
    posts = await db["posts"].find().to_list(1000)
    return posts


# new post
@app.post("/blog", response_description="Added new post", response_model=Post)
async def create_post(post: Post = Body(...)):
    post = jsonable_encoder(post)
    new_post = await db["posts"].insert_one(post)
    created_post = await db["posts"].find_one({"_id": new_post.inserted_id})
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_post)
    return created_post


# find post by id: get from  database
@app.get("/blog/{post_id}", response_description="Get a single post", response_model=Post)
async def show_post(post_id: int):
    if (post := await db["posts"].find_one({"id": post_id})) is not None:
        return post
    raise HTTPException(status_code=404, detail=f"Post {post_id} not found")


# update post
@app.put("/blog/{id}", response_description="Update a post", response_model=Post)
async def update_post(id: int, post: Post = Body(...)):
    post = {k: v for k, v in post.dict().items() if v is not None}

    if len(post) >= 1:
        update_result = await db["posts"].update_one({"id": id}, {"$set": post})

        if update_result.modified_count == 1:
            if (
                    updated_post := await db["posts"].find_one({"id": id})
            ) is not None:
                return updated_post

    if (existing_post := await db["posts"].find_one({"id": id})) is not None:
        return existing_post

    raise HTTPException(status_code=404, detail=f"Post {id} not found")


@app.delete("/blog/{id}", response_description="Delete a post")
async def delete_student(id: int):
    delete_result = await db["posts"].delete_one({"id": id})

    if delete_result.deleted_count == 1:
        return {"message": "Post has been deleted succesfully"}
        # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Post {id} not found")
