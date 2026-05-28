from fastapi import FastAPI, Depends, HTTPException, status,APIRouter,Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt import create_access_token
from schema.user_schema import Token,LoginRequest,TokenData
from auth.current_user import get_current_user
from model.user_model import User
from database.database import get_db
from auth.hash_password import verify_password
import json

router = APIRouter(
    prefix="/v1/login",
    tags=["Login"]
)
 
@router.post("/")
def login_for_access_token(form_data: LoginRequest,response:Response, db: Session = Depends(get_db)):
    try:

        user = db.query(User).filter(User.user_name==form_data.username).first()
        if not user:
            raise HTTPException(status_code=404,detail=f"user name {form_data.username} not found")
        
        if not verify_password(form_data.password,user.password):
            raise HTTPException(status_code=400,detail="password is incorrect")

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_data=TokenData(user_name=user.user_name,
                            user_email=user.user_email,
                            user_id=user.user_id,
                            user_role=user.user_role)
        access_token = create_access_token(data={"user_name": user.user_name,"user_email":user.user_email,"user_id":user.user_id,"user_role":user.user_role})
        response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,
    max_age=3600,
    samesite="lax",
    secure=False,
    path="/",
)

        return {"user_detail":user_data,"access_token":access_token}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")

@router.get("/")
def logout(response: Response):
    response.delete_cookie(key="session_id")
    return {"message": "Successfully logged out"}