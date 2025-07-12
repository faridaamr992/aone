from fastapi import APIRouter, HTTPException
from typing import List
from models.product import ProductModel, ProductCreateModel, ProductUpdateModel
from controllers.product_controller import (
    create_product_logic, get_all_products_logic,
    get_product_logic, update_product_logic, delete_product_logic
)

router = APIRouter()

@router.post("/create_product", response_model=ProductModel)
async def create_product(product: ProductCreateModel):
    try:
        return await create_product_logic(product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"create_product route: {str(e)}")

@router.get("/get_products", response_model=List[ProductModel])
async def get_products():
    try:
        return await get_all_products_logic()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get_products route: {str(e)}")

@router.get("/get_product/{product_id}", response_model=ProductModel)
async def get_product(product_id: str):
    try:
        return await get_product_logic(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get_product route: {str(e)}")

@router.put("/update_product/{product_id}")
async def update_product(product_id: str, data: ProductUpdateModel):
    try:
        return await update_product_logic(product_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"update_product route: {str(e)}")

@router.delete("/delete_product/{product_id}")
async def delete_product(product_id: str):
    try:
        return await delete_product_logic(product_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete_product route: {str(e)}")
