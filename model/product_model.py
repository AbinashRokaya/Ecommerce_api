from sqlalchemy import Column,String,Integer,ForeignKey,DECIMAL,DateTime
from database.database import Base
from sqlalchemy.sql import func
from model.category_model import Category
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer,primary_key=True,autoincrement=True)
    product_name = Column(String(50),nullable=False)
    product_price = Column(DECIMAL,nullable=False)
    product_description = Column(String(250))
    product_category = Column(Integer,ForeignKey("category.category_id"))
    product_quantity = Column(Integer,default=0)

    product_created_at = Column(DateTime,server_default=func.now())
    product_updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())


    category_rel = relationship("Category",back_populates="product_rel")
    cart_item_rel = relationship("CartItem",back_populates="product_rel")
    order_item_rel = relationship("OrderItem", back_populates="product_rel")