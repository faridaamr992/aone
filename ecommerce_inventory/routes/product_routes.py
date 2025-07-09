from fastapi import APIRouter, HTTPException
from database import db, to_object_id
from models.product import ProductModel, ProductUpdateModel, ProductCreateModel
from bson import ObjectId
from fastapi.responses import JSONResponse
from typing import List

router = APIRouter()

@router.post("/create_product", response_model=ProductModel)
async def create_product(product: ProductCreateModel):
    try:
        # Check if category exists by name
        category = await db.categories.find_one({"name": product.category_name})
        if not category:
            # Auto-create category
            new_cat = {"name": product.category_name, "description": ""}
            result = await db.categories.insert_one(new_cat)
            category_id = str(result.inserted_id)
        else:
            category_id = str(category["_id"])

        # Insert product with resolved category_id
        new_product = {
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "category_id": category_id
        }

        result = await db.products.insert_one(new_product)
        new_product["_id"] = str(result.inserted_id)
        return ProductModel(**new_product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"create product: {str(e)}")

@router.get("/get_products", response_model=List[ProductModel])
async def get_products():
    try:
        products = []
        async for product in db.products.find():
            product["_id"] = str(product["_id"])  # Convert ObjectId to string
            products.append(ProductModel(**product))
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get products: {str(e)}")
    
@router.get("/get_product/{product_id}", response_model=ProductModel)
async def get_product(product_id: str):
    try:
        obj_id = to_object_id(product_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")
        
        product = await db.products.find_one({"_id": obj_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        return ProductModel(**product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get product: {str(e)}")

@router.put("/update_product/{product_id}")
async def update_product(product_id: str, data: ProductUpdateModel):
    try:
        obj_id = to_object_id(product_id)
        result = await db.products.update_one({"_id": obj_id}, {"$set": data.dict(exclude_unset=True)})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found or not updated")
        return {"msg": "Updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"update product")

@router.delete("/delete_product/{product_id}")
async def delete_product(product_id: str):
    try:
        obj_id = to_object_id(product_id)
        result = await db.products.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"msg": "Deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete product")
