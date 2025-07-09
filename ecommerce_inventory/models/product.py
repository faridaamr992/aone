from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

# For reading from DB
class ProductModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    price: float
    stock: int
    category_id: str  # internal use only, used to store in MongoDB

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

# For creating new products (required category name only)
class ProductCreateModel(BaseModel):
    name: str
    price: float
    stock: int
    category_name: str  # required instead of category_id

# For partial updates
class ProductUpdateModel(BaseModel):
    name: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category_name: Optional[str]  # optional update for category
