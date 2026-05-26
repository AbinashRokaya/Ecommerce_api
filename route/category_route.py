from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
import json
from schema.category_schema import CategoryRequest,CategoryResponse,CategoryResponseList
from auth.current_user import get_current_user,require_permission
from sqlalchemy.orm import Session
from model.category_model import Category
from schema.user_schema import TokenData
from database.database import get_db


router =  APIRouter(
    prefix="/v1/categorys",
    tags=["Category"]
)

@router.post("/add")
def create_category(request:CategoryRequest,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:
        category = db.query(Category).filter(Category.category_name==request.category_name).first()

        if category:
            raise HTTPException(status_code=409,detail=f"category {request.category_name} is alredy exist")
        
        new_category = Category(
            category_name = request.category_name,
            category_description = request.category_description
        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        product_res = CategoryResponse(
           category_id=category.category_id,
    category_name=category.category_name,
    category_description=category.category_description

        )

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": "new category is created",
                "data": product_res.model_dump()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    

@router.put("/edit/{id}")
def create_product(id:int,request:CategoryRequest,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:
        category = db.query(Category).filter(Category.category_id==id).first()

        if not category:
            raise HTTPException(status_code=409,detail=f"product id {id} not found")
        
        
        category.category_name=request.category_name
        category.category_description=request.category_description

    
        
        db.commit()
        db.refresh(category)

        product_res = CategoryResponse(
           category_id=category.category_id,
    category_name=category.category_name,
    category_description=category.category_description

        )

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": f"Category id {id} is updated successfully",
                "data": product_res.model_dump()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")



@router.get("/")
def get_category(db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:
        category = db.query(Category).all()
        if not category:
            raise HTTPException(status_code=404,detail="category not found")
        

        category_list=[
            CategoryResponse(
                category_id=c.category_id,
    category_name=c.category_name,
    category_description=c.category_description


            )for c in category
        ]
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": "all caotegory list",
                    "data": CategoryResponseList(category_list=category_list).model_dump()
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    

@router.get("/{id}")
def get_product(id:int,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:

        category = db.query(Category).filter(Category.category_id==id).first()

        if not category:
            raise HTTPException(status_code=404,detail=f"products id {id} not found")
        
        category_list =[
            CategoryResponse(
            category_id=category.category_id,
            category_name = category.category_name,
            category_description = category.category_description
            )

        ]
            

        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "status_code": 200,
                "message": f"{id} product",
                "data": CategoryResponseList(category_list=category_list).model_dump()
            }
        )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
@router.delete("/{id}")
def delete_category(id:int,db:Session=Depends(get_db),current_user= Depends(require_permission("edit"))):
    try:
        category = db.query(Category).filter(Category.category_id==id).first()
        
        if not category:
            raise HTTPException(status_code=404,detail=f"category id {id} not found")
        
        db.delete(category)
        db.commit()
        
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": f"{id} category deleted",
                    "data": ""
                }
            )


    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    
