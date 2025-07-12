from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()  

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.user_db
collection = db.users

app = FastAPI()

# Pydantic model (custom integer ID instead of ObjectId)
class User(BaseModel):
    id: int
    name: str = Field(default="Farida")
    age: int = Field(default=23)

# Helper function
def user_helper(user) -> dict:
    return {
        "id": user["_id"],  # your custom int id will be used as _id
        "name": user["name"],
        "age": user["age"]
    }

from pymongo import MongoClient
from bson import ObjectId

client = MongoClient(MONGO_URI)
db = client.user_db
collection = db.users

# Delete all documents where _id is of type ObjectId
collection.delete_many({"_id": {"$type": "objectId"}})


# POST - Create User
@app.post("/Create", response_model=User)
def create_user(user: User):
    if collection.find_one({"_id": user.id}):
        raise HTTPException(status_code=400, detail="User with this ID already exists")
    collection.insert_one({
        "_id": user.id,
        "name": user.name,
        "age": user.age
    })
    return user

# GET - All users
@app.get("/Get_Users", response_model=List[User])
def get_users():
    users = []
    for user in collection.find():
        try:
            users.append(user_helper(user))
        except Exception:
            continue  # skip malformed records
    return users


# GET - One user by custom ID
@app.get("/Get_User/{user_id}", response_model=User)
def get_user(user_id: int):
    user = collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

# PUT - Update user
@app.put("/Update/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    result = collection.update_one(
        {"_id": user_id},
        {"$set": {
            "name": updated_user.name,
            "age": updated_user.age
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# DELETE - Delete user
@app.delete("/Delete/{user_id}")
def delete_user(user_id: int):
    result = collection.delete_one({"_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
