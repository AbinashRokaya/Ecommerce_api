from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from schema.user_schema import UserRequest,UserResponse
from auth.current_user import get_current_user,require_permission
from database.database import get_db
from sqlalchemy.orm import Session
from model.user_model import User
from model.product_model import Product
from auth.hash_password import hash_password_user
from schema.product_schema import ProductRequest,ProductResponse,ProductResponseList
import json
from typing import List

router =  APIRouter(
    prefix="/v1/products",
    tags=["Products"]
)

@router.post("/add")
def create_product(request:ProductRequest,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
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

        product_res = ProductResponse(
            product_id =new_product.product_id,
    product_name = new_product.product_name,
    product_price =new_product.product_price,
    product_description = new_product.product_description,
    product_category = new_product.product_category,
    product_quantity = new_product.product_quantity,
    product_category_name=new_product.category_rel.category_name

        )

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": "new product is created",
                "data": product_res.model_dump()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")


@router.put("/edit/{id}")
def create_product(id:int,request:ProductRequest,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:
        product = db.query(Product).filter(Product.product_id==id).first()

        if not product:
            raise HTTPException(status_code=409,detail=f"product id {id} not found")
        
        
        product.product_name = request.product_name,
        product.product_price = request.product_price,
        product.product_description = request.product_description,
        product.product_category = request.product_category,
        product.product_quantity = request.product_quantity
    
        
        db.commit()
        db.refresh(product)

        product_res = ProductResponse(
            product_id =product.product_id,
    product_name = product.product_name,
    product_price =product.product_price,
    product_description = product.product_description,
    product_category = product.product_category,
    product_quantity = product.product_quantity,
     product_category_name=product.category_rel.category_name
        )

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": f"product id {id} is updated successfully",
                "data": product_res.model_dump()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")




@router.get("/")
def get_product(db:Session=Depends(get_db),current_user= Depends(require_permission("view"))):
    try:

        products = db.query(Product).all()

        if not products:
            raise HTTPException(status_code=404,detail="products not found")
        
        product_list =[
            ProductResponse(
                product_id =p.product_id,
    product_name = p.product_name,
    product_price =p.product_price,
    product_description = p.product_description,
    product_category = p.product_category,
    product_quantity = p.product_quantity,
     product_category_name=p.category_rel.category_name
            )for p in products

        ]
            

        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "status_code": 200,
                "message": "new product is created",
                "data": ProductResponseList(product_list=product_list).model_dump()
            }
        )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")


@router.get("/{id}")
def get_product(id:int,db:Session=Depends(get_db),current_user= Depends(require_permission("view"))):
    try:

        products = db.query(Product).filter(Product.product_id==id).first()

        if not products:
            raise HTTPException(status_code=404,detail=f"products id {id} not found")
        
        product_list =[
            ProductResponse(
                product_id =products.product_id,
    product_name = products.product_name,
    product_price =products.product_price,
    product_description = products.product_description,
    product_category = products.product_category,
    product_quantity = products.product_quantity,
     product_category_name=products.category_rel.category_name
            )

        ]
            

        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "status_code": 200,
                "message": f"{id} product",
                "data": ProductResponseList(product_list=product_list).model_dump()
            }
        )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")


@router.delete("/{id}")
def delete_product(id:int,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:
        product = db.query(Product).filter(Product.product_id==id).first()
        
        if not product:
            raise HTTPException(status_code=404,detail=f"product id {id} not found")
        
        db.delete(product)
        db.commit()
        
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": f"{id} product deleted",
                    "data": ""
                }
            )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")