from fastapi import FastAPI, Depends, HTTPException, status,APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt import create_access_token
from schema.user_schema import Token
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
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
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
        access_token = create_access_token(data={"user_name": user.user_name,"user_email":user.user_email,"user_id":user.user_id})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")