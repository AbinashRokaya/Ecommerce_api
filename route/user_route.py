from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from schema.user_schema import UserRequest,UserResponse
from auth.current_user import get_current_user
from database.database import get_db
from sqlalchemy.orm import Session
from model.user_model import User
from auth.hash_password import hash_password_user
import json


router =  APIRouter(
    prefix="/v1/users",
    tags=["User"]
)

@router.post("/")
def create_user(request:UserRequest,db:Session=Depends(get_db)):
    try:
        user_email = db.query(User).filter(User.user_email==request.user_email).first()

        if user_email:
            raise HTTPException(status_code=409,detail=f"user with email {request.user_email} alredy exist. try new email id")
        
        hased_password = hash_password_user(request.password)

        new_user = User(
            user_name = request.user_name,
            user_address = request.user_address,
            user_email = request.user_email,
            password = hased_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        user_response = UserResponse(
            user_name = new_user.user_name,
            user_address = new_user.user_address,
            user_email = new_user.user_email
        )

        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "status_code": 201,
                "message": "new user is created",
                "data": user_response.model_dump()
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
    

@router.get("/me")
def read_user_me(current_user= Depends(get_current_user)):
    print(current_user)
    return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "status_code": 200,
                "message": "detail of me",
                "data": current_user.model_dump()
            }
        )


    

