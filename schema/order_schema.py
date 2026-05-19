from pydantic import BaseModel,Field
from typing import Optional,List
from decimal import Decimal

class OrderRequest(BaseModel):
    order_amount : Decimal=Field(gt=0,decimal_places=2)
    

class OrderItemRequest(BaseModel):
    product_id : int
    quantity : int

class OrderItemRequestList(BaseModel):
    order_items : List[OrderItemRequest]

class OrderResponse(BaseModel):
    order_id : int
    order_amount : int
    order_user_id : int

class OrderItemResponse(BaseModel):
    order_item_id : int
    order_id : int
    product_id : int
    quantity : int
    price : int

class orderItemResponseList(BaseModel):
    order : OrderResponse
    order_item : List[OrderItemResponse]

class OrderResponseList(BaseModel):
    order_list : List[OrderResponse]

class GetOrderIResponseList(BaseModel):
    list_all_item : List[orderItemResponseList]

