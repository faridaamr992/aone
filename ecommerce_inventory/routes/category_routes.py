from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId
from database import db, to_object_id
from models.category import CategoryModel, CategoryCreateModel, CategoryUpdateModel

router = APIRouter()

@router.post("/create_category", response_model=CategoryModel)
async def create_category(category: CategoryCreateModel):
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


@router.get("/get_categories", response_model=List[CategoryModel])
async def get_categories():
    try:
        categories = []
        async for cat in db.categories.find():
            cat["_id"] = str(cat["_id"])
            categories.append(CategoryModel(**cat))
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get categories: {str(e)}")


@router.get("/get_category/{category_id}", response_model=CategoryModel)
async def get_category(category_id: str):
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


@router.put("/update_category/{category_id}")
async def update_category(category_id: str, data: CategoryUpdateModel):
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


@router.delete("/delete_category/{category_id}")
async def delete_category(category_id: str):
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
