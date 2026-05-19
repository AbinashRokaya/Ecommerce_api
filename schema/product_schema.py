from pydantic import BaseModel,Field
from typing import Optional
from decimal import Decimal

class ProductRequest(BaseModel):
    product_name : str = Field(max_length=50)
    product_price : Decimal = Field(gt=0,decimal_places=2)
    product_description : str = Field(max_length=250)
    product_category : int 
    product_quantity : int