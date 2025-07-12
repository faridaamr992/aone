from fastapi import HTTPException
from core.database import db, to_object_id
from models.product import ProductModel, ProductCreateModel, ProductUpdateModel

async def create_product_logic(product: ProductCreateModel):
    try:
        category = await db.categories.find_one({"name": product.category_name})
        if not category:
            new_cat = {"name": product.category_name, "description": ""}
            result = await db.categories.insert_one(new_cat)
            category_id = str(result.inserted_id)
        else:
            category_id = str(category["_id"])

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

async def get_all_products_logic():
    try:
        products = []
        async for product in db.products.find():
            product["_id"] = str(product["_id"])
            products.append(ProductModel(**product))
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get products: {str(e)}")

async def get_product_logic(product_id: str):
    try:
        obj_id = to_object_id(product_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        product = await db.products.find_one({"_id": obj_id})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        product["_id"] = str(product["_id"])
        return ProductModel(**product)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get product: {str(e)}")

async def update_product_logic(product_id: str, data: ProductUpdateModel):
    try:
        obj_id = to_object_id(product_id)
        result = await db.products.update_one({"_id": obj_id}, {"$set": data.dict(exclude_unset=True)})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Product not found or not updated")
        return {"msg": "Updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"update product: {str(e)}")

async def delete_product_logic(product_id: str):
    try:
        obj_id = to_object_id(product_id)
        result = await db.products.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"msg": "Deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete product: {str(e)}")
