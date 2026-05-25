from sqlalchemy import Column,String,Integer,ForeignKey,DateTime,Enum
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from schema.user_schema import Role_schema

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer,primary_key=True,autoincrement=True)
    user_name = Column(String(50),nullable=False)
    user_address = Column(String(50),nullable=False)
    user_email = Column(String(50),nullable=False)
    password = Column(String(255),nullable=False)
    user_role = Column(Enum(Role_schema),default=Role_schema.User)

    user_created_at = Column(DateTime,server_default=func.now())
    user_updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())

    
    payment_rel = relationship("Payment",back_populates="user_rel")
    order_rel = relationship("Order",back_populates="user_rel")
    cart_rel = relationship("Cart",back_populates="user_rel")

