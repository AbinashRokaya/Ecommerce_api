from pydantic import BaseModel,Field
from typing import Optional

class CategoryRequest(BaseModel):
    category_name:str=Field(max_length=50)
    category_description:Optional[str]=Field(max_length=250)
    