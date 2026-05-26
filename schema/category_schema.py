from pydantic import BaseModel,Field
from typing import Optional,List

class CategoryRequest(BaseModel):
    category_name:str=Field(max_length=50)
    category_description:Optional[str]=Field(max_length=250)


class CategoryResponse(BaseModel):
    category_id:int
    category_name:str
    category_description:str

class CategoryResponseList(BaseModel):
    category_list:List[CategoryResponse]
    