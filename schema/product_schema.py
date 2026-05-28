from pydantic import BaseModel,Field
from typing import Optional,List
from decimal import Decimal

class ProductRequest(BaseModel):
    product_name : str = Field(max_length=50)
    product_price : int = Field(gt=0)
    product_description : str = Field(max_length=250)
    product_category : int
   
    product_quantity : int

    
class ProductResponse(BaseModel):
    product_id : int
    product_name : str = Field(max_length=50)
    product_price : int = Field(gt=0)
    product_description : str = Field(max_length=250)
    product_category : int 
    product_quantity : int
    product_category_name:Optional[str]=None

 



class ProductResponseList(BaseModel):
    product_list : List[ProductResponse]