from pydantic import BaseModel, Field
from typing import Optional

# Model for reading orders
class OrderModel(BaseModel):
    id: Optional[str] = Field(alias="_id")  # _id from MongoDB as string
    product_id: str
    quantity: int
    status: str

    class Config:
        populate_by_name = True  # Allows alias _id to be used as id in JSON

# Model for creating new orders
class OrderCreateModel(BaseModel):
    product_name: str 
    quantity: int
    status: Optional[str] = "pending"

# Model for updating existing orders
class OrderUpdateModel(BaseModel):
    product_id: Optional[str]
    quantity: Optional[int]
    status: Optional[str]
