from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from schema.order_schema import (OrderRequest,OrderItemRequest,
                                 OrderItemRequestList,OrderItemResponse,
                                 OrderResponse,orderItemResponseList,
                                 GetOrderIResponseList)
from auth.current_user import get_current_user
from database.database import get_db
from sqlalchemy.orm import Session
from model.product_model import Product
from model.order_model import Order,OrderItem
import json
from model.user_model import User


router =  APIRouter(
    prefix="/v1/orders",
    tags=["Orders"]
)

@router.post("/")
def create_order(request:OrderItemRequestList,db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    
    try:
        for item in request.order_items:
            product = db.query(Product).filter(Product.product_id==item.product_id).first()

            if not product:
                raise HTTPException(status_code=404,detail=f"product not found")

            if not item.quantity<=product.product_quantity:
                raise HTTPException(status_code=400,detail=f"product {product.product_name} access the limit")
            

        order = Order(
            order_amount = 0,
            order_user_id = current_user.user_id
        )
        db.add(order)
        db.commit()
        

        total_amount = 0
        created_order_items = []

        for item in request.order_items:
            product = db.query(Product).filter(Product.product_id==item.product_id).first()

            price = product.product_price*item.quantity
            total_amount=total_amount+price

            product.product_quantity=product.product_quantity-item.quantity
            db.commit()

            order_item = OrderItem(
                order_id = order.order_id,
                product_id = product.product_id,
                quantity = item.quantity,
                price=price
            )
            db.add(order_item)
            db.commit()
            db.refresh(order_item)
            created_order_items.append(order_item)


        order.order_amount = total_amount
        db.commit()
        db.refresh(order)

        new_order = OrderResponse(
            order_id = order.order_id,
        order_amount = order.order_amount,
        order_user_id = order.order_user_id
        )
        order_item = [OrderItemResponse(
            order_item_id = o.id,
        order_id = o.order_id,
        product_id = o.product_id,
        quantity = o.quantity,
        price = o.price
        ) for o in created_order_items]



        order_item_list = orderItemResponseList(
            order=new_order,
            order_item=order_item
        )

        
        return JSONResponse(
                status_code=201,
                content={
                    "success": True,
                    "status_code": 201,
                    "message": "new order is created",
                    "data": order_item_list.model_dump()
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")

@router.get("/me")
def get_order_me(db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:
        orders = db.query(Order).filter(Order.order_user_id==current_user.user_id).all()

        new_item =[]
        for order in orders:
            order_items = db.query(OrderItem).filter(OrderItem.order_id==order.order_id).all()
        

            new_order = OrderResponse(
                order_id = order.order_id,
            order_amount = order.order_amount,
            order_user_id = order.order_user_id
            )
            order_item = [OrderItemResponse(
                order_item_id = o.id,
            order_id = o.order_id,
            product_id = o.product_id,
            quantity = o.quantity,
            price = o.price
            ) for o in order_items]

            order_item_list = orderItemResponseList(
                order=new_order,
                order_item=order_item
            )
            new_item.append(order_item_list)
        
        get_all = GetOrderIResponseList(list_all_item=new_item)

        
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": f"all the list order of user id {current_user.user_id}",
                    "data": get_all.model_dump()
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")

@router.get("/all")
def get_order_me(db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:
        orders = db.query(Order).all()
    
        new_item =[]
        for order in orders:
            order_items = db.query(OrderItem).filter(OrderItem.order_id==order.order_id).all()
            

            new_order = OrderResponse(
                order_id = order.order_id,
            order_amount = order.order_amount,
            order_user_id = order.order_user_id
            )
            order_item = [OrderItemResponse(
                order_item_id = o.id,
            order_id = o.order_id,
            product_id = o.product_id,
            quantity = o.quantity,
            price = o.price
            ) for o in order_items]

            order_item_list = orderItemResponseList(
                order=new_order,
                order_item=order_item
            )
            new_item.append(order_item_list)
        
        get_all = GetOrderIResponseList(list_all_item=new_item)

        
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": "all the list of order",
                    "data": get_all.model_dump()
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")

