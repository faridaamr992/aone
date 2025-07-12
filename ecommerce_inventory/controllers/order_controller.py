from fastapi import HTTPException
from bson import ObjectId
from core.database import db, to_object_id
from models.order import OrderModel, OrderCreateModel, OrderUpdateModel

async def create_order_logic(order: OrderCreateModel):
    try:
        product = await db.products.find_one({"name": order.product_name})
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.get("stock", 0) < order.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        new_order = {
            "product_id": str(product["_id"]),
            "quantity": order.quantity,
            "status": order.status or "pending"
        }
        result = await db.orders.insert_one(new_order)

        await db.products.update_one(
            {"_id": product["_id"]},
            {"$inc": {"stock": -order.quantity}}
        )

        new_order["_id"] = str(result.inserted_id)
        return OrderModel(**new_order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"create order: {str(e)}")

async def get_all_orders_logic():
    try:
        orders = []
        async for order in db.orders.find():
            order["_id"] = str(order["_id"])
            orders.append(OrderModel(**order))
        return orders
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get orders: {str(e)}")

async def get_order_logic(order_id: str):
    try:
        obj_id = to_object_id(order_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        order = await db.orders.find_one({"_id": obj_id})
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        order["_id"] = str(order["_id"])
        return OrderModel(**order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get order: {str(e)}")

async def update_order_logic(order_id: str, data: OrderUpdateModel):
    try:
        obj_id = to_object_id(order_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        update_data = data.dict(exclude_unset=True)

        if "product_id" in update_data:
            if not await db.products.find_one({"_id": ObjectId(update_data["product_id"])}):
                raise HTTPException(status_code=404, detail="Product not found")

        result = await db.orders.update_one({"_id": obj_id}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Order not found or not updated")
        return {"msg": "Updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"update order: {str(e)}")

async def delete_order_logic(order_id: str):
    try:
        obj_id = to_object_id(order_id)
        if not obj_id:
            raise HTTPException(status_code=400, detail="Invalid ObjectId")

        result = await db.orders.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"msg": "Deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete order: {str(e)}")
