from fastapi import APIRouter, HTTPException
from typing import List
from models.order import OrderModel, OrderCreateModel, OrderUpdateModel
from controllers.order_controller import (
    create_order_logic, get_all_orders_logic,
    get_order_logic, update_order_logic, delete_order_logic
)

router = APIRouter()

@router.post("/create_order", response_model=OrderModel)
async def create_order(order: OrderCreateModel):
    try:
        return await create_order_logic(order)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"create_order route: {str(e)}")

@router.get("/get_orders", response_model=List[OrderModel])
async def get_orders():
    try:
        return await get_all_orders_logic()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get_orders route: {str(e)}")

@router.get("/get_order/{order_id}", response_model=OrderModel)
async def get_order(order_id: str):
    try:
        return await get_order_logic(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"get_order route: {str(e)}")

@router.put("/update_order/{order_id}")
async def update_order(order_id: str, data: OrderUpdateModel):
    try:
        return await update_order_logic(order_id, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"update_order route: {str(e)}")

@router.delete("/delete_order/{order_id}")
async def delete_order(order_id: str):
    try:
        return await delete_order_logic(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete_order route: {str(e)}")
