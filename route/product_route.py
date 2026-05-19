from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from schema.user_schema import UserRequest,UserResponse
from auth.current_user import get_current_user
from database.database import get_db
from sqlalchemy.orm import Session
from model.user_model import User
from model.product_model import Product
from auth.hash_password import hash_password_user
from schema.product_schema import ProductRequest
import json


router =  APIRouter(
    prefix="/v1/products",
    tags=["Products"]
)

@router.post("/")
def create_product(request:ProductRequest,db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:
        product = db.query(Product).filter(Product.product_name==request.product_name).first()

        if product:
            raise HTTPException(status_code=409,detail=f"product {request.product_name} alredy exists")
        
        new_product = Product(
            product_name = request.product_name,
            product_price = request.product_price,
            product_description = request.product_description,
            product_category = request.product_category,
            product_quantity = request.product_quantity
        )
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": "new product is created",
                "data": new_product.model_dump()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
@router.get("/")
def get_product(db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:

        products = db.query(Product).all()

        if not products:
            raise HTTPException(status_code=404,detail="products not found")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "status_code": 200,
                "message": "new product is created",
                "data": products.model_dump()
            }
        )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
