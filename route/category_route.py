from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
import json
from schema.category_schema import CategoryRequest
from auth.current_user import get_current_user
from sqlalchemy.orm import Session
from model.category_model import Category
from schema.user_schema import TokenData
from database.database import get_db


router =  APIRouter(
    prefix="/v1/categorys",
    tags=["Category"]
)

@router.post("/")
def create_category(request:CategoryRequest,db:Session=Depends(get_db),current_user= Depends(get_current_user)):
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

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": "new category is created",
                "data": new_category.model_dump()
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    

@router.get("/")
def get_category(db:Session=Depends(get_db),current_user= Depends(get_current_user)):
    try:
        category = db.query(Category).all()
        if not category:
            raise HTTPException(status_code=404,detail="category not found")
        return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "status_code": 200,
                    "message": "all caotegory list",
                    "data": category.model_dump()
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")