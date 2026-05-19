from fastapi import FastAPI,status,HTTPException

from fastapi.responses import JSONResponse
import uvicorn
from database.database import Base,engine

from route import user_route
from route import login_route
from route import category_route
from route import product_route
from route import order_route
from route import cart_route

from model.user_model import User
from model.cart_model import Cart
from model.category_model import Category
from model.order_model import Order
from model.product_model import Product
from model.payment_model import Payment







app=FastAPI()

app.include_router(user_route.router)
app.include_router(login_route.router)
app.include_router(category_route.router)
app.include_router(product_route.router)
app.include_router(order_route.router)
app.include_router(cart_route.router)





if __name__=="__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True,loop="asyncio")
