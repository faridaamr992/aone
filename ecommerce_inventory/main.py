from fastapi import FastAPI
from views import product_routes, category_routes, order_routes

app = FastAPI(title="E-commerce Inventory API")

app.include_router(product_routes.router, prefix="/products", tags=["Products"])
app.include_router(category_routes.router, prefix="/categories", tags=["Categories"])
app.include_router(order_routes.router, prefix="/orders", tags=["Orders"])
