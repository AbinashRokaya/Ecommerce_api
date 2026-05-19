from pydantic import BaseModel
from typing import List


class CartRequest(BaseModel):
    cart_id:int
    cart_user_id:int

    
class CartItemRequest(BaseModel):
    product_id : int
    quantity : int

class CartResponse(BaseModel):
    cart_id:int
    cart_user_id:int

class CartItemResponse(BaseModel):
    id : int
    cart_id : int
    product_id : int
    quantity : int

class CartItemResponseList(BaseModel):
    cart : CartResponse
    cart_item : List[CartItemResponse]
