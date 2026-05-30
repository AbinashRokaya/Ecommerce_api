from pydantic import BaseModel,Field
from typing import Optional,List
from decimal import Decimal

class ProductRequest(BaseModel):
    product_name : str = Field(max_length=50)
    product_price : int = Field(gt=0)
    product_description : str = Field(max_length=250)
    product_category : int
    product_image_url:str
   
    product_quantity : int

    
class ProductResponse(BaseModel):
    product_id : int
    product_name : str = Field(max_length=50)
    product_price : int = Field(gt=0)
    product_description : str = Field(max_length=250)
    product_category : int 
    product_quantity : int
    product_image_url:str | None = None
    product_category_name:Optional[str]=None

 



class ProductResponseList(BaseModel):
    product_list : List[ProductResponse]


class ProductImageResponse(BaseModel):
    original_name: str
    saved_as: str
    url: str
    type: str