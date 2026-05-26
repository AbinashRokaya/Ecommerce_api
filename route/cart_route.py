from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from schema.cart_schema import (CartItemRequest,CartItemResponse,
                                CartRequest,CartResponse,CartItemResponseList)
from auth.current_user import get_current_user
from database.database import get_db
from sqlalchemy.orm import Session
from model.order_model import Order,OrderItem
from model.cart_model import Cart,CartItem
from model.product_model import Product

import json


router =  APIRouter(
    prefix = "/v1/carts",
    tags = ["Carts"]
)

@router.post("/")
def create_cart(request:CartItemRequest,db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:
        product = db.query(Product).filter(Product.product_id==request.product_id).first()

        if not product:
            raise HTTPException(status_code=404,detail="product not found")
        
        cart_item=db.query(CartItem).filter(CartItem.product_id==product.product_id).first()

        cart_user = db.query(Cart).filter(Cart.cart_user_id==current_user.user_id).first()
        if not cart_item:

            
            if not cart_user:
                cart_user = Cart(
                    cart_user_id = current_user.user_id
                )
                db.add(cart_user)
                db.commit()
                db.refresh(cart_user)

            cart_item = CartItem(
                cart_id = cart_user.cart_id,
                product_id = request.product_id,
                quantity = request.quantity
            )
            db.add(cart_item)
            db.commit()
            db.refresh(cart_item)
        else:
            cart_item.quantity=request.quantity

            db.commit()
            db.refresh(cart_item)

        cart_response = CartResponse(
            cart_id = cart_user.cart_id,
            cart_user_id = cart_user.cart_user_id
        )
        cart_item_response = [CartItemResponse(
            id = cart_item.id,
            cart_id = cart_item.cart_id,
            product_id = cart_item.product_id,
            quantity =  cart_item.quantity,
        )]

        list_cart = CartItemResponseList(
            cart = cart_response,
            cart_item = cart_item_response
        )
        return JSONResponse(
                status_code=201,
                content={
                    "success": True,
                    "status_code": 201,
                    "message": "new cart is created",
                    "data": list_cart.model_dump()
                }
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    

    
@router.get("/me")
def get_cart_me(db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:
        cart_user = db.query(Cart).filter(Cart.cart_user_id==current_user.user_id).first()
        
        if not cart_user:
            cart_user = Cart(
                cart_user_id = current_user.user_id
            )
            db.add(cart_user)
            db.commit()
            db.refresh(cart_user)


        cart_items = db.query(CartItem).filter(CartItem.cart_id==cart_user.cart_id).all()

        cart_response = CartResponse(
            cart_id = cart_user.cart_id,
            cart_user_id = cart_user.cart_user_id
        )

        cart_item_response = [CartItemResponse(
            id = cart_item.id,
            cart_id = cart_item.cart_id,
            product_id = cart_item.product_id,
            quantity =  cart_item.quantity,
        )for cart_item in cart_items]

        list_cart = CartItemResponseList(
            cart = cart_response,
            cart_item = cart_item_response
        )

        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": "list of cart product",
                    "data": list_cart.model_dump()
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
