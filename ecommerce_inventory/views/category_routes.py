from fastapi import APIRouter, HTTPException
from typing import List
from models.category import CategoryModel, CategoryCreateModel, CategoryUpdateModel
from controllers.category_controller import (
    create_category_controller,
    get_categories_controller,
    get_category_controller,
    update_category_controller,
    delete_category_controller
)

router = APIRouter()

@router.post("/create_category", response_model=CategoryModel)
async def create_category(category: CategoryCreateModel):
    try:
        return await create_category_controller(category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_categories", response_model=List[CategoryModel])
async def get_categories():
    try:
        return await get_categories_controller()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_category/{category_id}", response_model=CategoryModel)
async def get_category(category_id: str):
    try:
        return await get_category_controller(category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_category/{category_id}")
async def update_category(category_id: str, data: CategoryUpdateModel):
    try:
        return await update_category_controller(category_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_category/{category_id}")
async def delete_category(category_id: str):
    try:
        return await delete_category_controller(category_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
