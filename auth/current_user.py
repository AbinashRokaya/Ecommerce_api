from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.jwt import verify_token
from schema.user_schema import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login")

def get_current_user(token:str=Depends(oauth2_scheme)):
    # print(token)
    payload = verify_token(token=token)
    user_name = payload.get("user_name")
    user_email = payload.get("user_email")
    # print(user_email,user_name)

    if user_name is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    if user_email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    # print(user_email,user_name)
    return TokenData(user_name=user_name,user_email=user_email)