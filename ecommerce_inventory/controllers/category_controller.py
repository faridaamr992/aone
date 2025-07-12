from fastapi import HTTPException
from typing import List, Optional
from bson import ObjectId
from core.database import db, to_object_id
from models.category import CategoryModel, CategoryCreateModel, CategoryUpdateModel

async def create_category_controller(category: CategoryCreateModel) -> CategoryModel:
    try:
        existing = await db.categories.find_one({"name": category.name})
        if existing:
            raise HTTPException(status_code=400, detail="Category already exists")

        new_cat = category.dict()
        result = await db.categories.insert_one(new_cat)
        new_cat["_id"] = str(result.inserted_id)
        return CategoryModel(**new_cat)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"create category: {str(e)}")

async def get_categories_controller() -> List[CategoryModel]:
    try:
        categories = []
        async for cat in db.categories.find():
            cat["_id"] = str(cat["_id"])
            categories.append(CategoryModel(**cat))
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get categories: {str(e)}")

async def get_category_controller(category_id: str) -> CategoryModel:
    try:
        obj_id = to_object_id(category_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        category = await db.categories.find_one({"_id": obj_id})
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        category["_id"] = str(category["_id"])
        return CategoryModel(**category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get category: {str(e)}")

async def update_category_controller(category_id: str, data: CategoryUpdateModel) -> dict:
    try:
        obj_id = to_object_id(category_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        update_data = data.dict(exclude_unset=True)
        result = await db.categories.update_one({"_id": obj_id}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Category not found or not updated")
        return {"msg": "Updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"update category: {str(e)}")

async def delete_category_controller(category_id: str) -> dict:
    try:
        obj_id = to_object_id(category_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        result = await db.categories.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        return {"msg": "Deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete category: {str(e)}")
