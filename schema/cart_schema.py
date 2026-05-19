from pydantic import BaseModel


class CartRequest(BaseModel):
    cart_id:int
    cart_user_id:int

    