from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not set")

# Connect to MongoDB
client = AsyncIOMotorClient(MONGO_URI)
db = client.ecommerce_db

def to_object_id(id: str):
    try:
        return ObjectId(id)
    except:
        return None

