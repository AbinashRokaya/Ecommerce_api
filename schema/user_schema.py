from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class UserRequest(BaseModel):
    user_name : str = Field(max_length=50)
    user_address : str = Field(max_length=50)
    user_email : EmailStr 
    password : str = Field(max_length=50)

class UserResponse(BaseModel):
    user_name : str = Field(max_length=50)
    user_address : str = Field(max_length=50)
    user_email : EmailStr 


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_name :str
    user_email : EmailStr
    user_id : int
    

    