from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer,primary_key=True,autoincrement=True)
    category_name = Column(String(50),nullable=False)
    category_description = Column(String(250))

    category_created_at = Column(DateTime,server_default=func.now())
    category_updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())

    product_rel = relationship("Product",back_populates="category_rel")