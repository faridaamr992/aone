from pydantic import BaseModel, Field
from typing import Optional

class CategoryModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        populate_by_name = True  # Allows returning _id as id
        json_encoders = {str: str}

class CategoryCreateModel(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryUpdateModel(BaseModel):
    name: Optional[str]
    description: Optional[str]
