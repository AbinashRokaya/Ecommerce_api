from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from fastapi.responses import JSONResponse
import json
from schema.category_schema import CategoryRequest,CategoryResponse,CategoryResponseList,CategoryImageResponse
from auth.current_user import get_current_user,require_permission
from sqlalchemy.orm import Session
from model.category_model import Category
from schema.user_schema import TokenData
from database.database import get_db

import os
import shutil
import uuid
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from dotenv import load_dotenv

load_dotenv()

cloudinary.config( 
    cloud_name = os.getenv("CLOUD_NAME"), 
    api_key =os.getenv("API_KEY"), 
    api_secret = os.getenv("API_SECRET"),
    secure=True
)


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
            category_description = request.category_description,
            category_image_url=request.category_image_url

        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        product_res = CategoryResponse(
           category_id=new_category.category_id,
    category_name=new_category.category_name,
    category_description=new_category.category_description,
    category_image_url=new_category.category_image_url

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
    category_description=c.category_description,
    category_image_url=c.category_image_url


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
            category_description = category.category_description,
            category_image_url=category.category_image_url
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
    


@router.post("/upload")
async def upload_image_category(file:UploadFile=File(...)):
    try:
        allowed_types = ["jpeg", "png", "gif", "webp"]
        
        ext=file.filename.split(".")[-1]
        if ext not in allowed_types:
            raise HTTPException(status_code=400,detail=f"{file.content_type} is not allowed")
        
    
        unique_name=f"{uuid.uuid4()}.{ext}"
        file_location=f"uploads/{unique_name}"
        file_content = await file.read()

        
        upload_result = cloudinary.uploader.upload(
            file_content,        
            public_id=f"category_{uuid.uuid4().hex}" 
        )
        
       
        cloud_url = upload_result.get("secure_url")
        unique_name = upload_result.get("public_id")

        

        image_detail = CategoryImageResponse(
            original_name=file.filename,
            saved_as=unique_name,
            url=cloud_url,
            type=file.content_type
        )
        return JSONResponse(
                        status_code=200,
                        content={
                            "success": True,
                            "status_code": 200,
                            "message": "successfully upload image",
                            "data": image_detail.model_dump()
                        }
                    )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")