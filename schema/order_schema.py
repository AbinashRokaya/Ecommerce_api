from pydantic import BaseModel,Field
from typing import Optional
from decimal import Decimal

class OrderRequest(BaseModel):
    order_amount:Decimal=Field(gt=0,decimal_places=2)
    


