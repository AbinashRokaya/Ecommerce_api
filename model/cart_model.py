from sqlalchemy import Column,String,Integer,ForeignKey,DateTime
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer,primary_key=True,autoincrement=True)
    cart_user_id = Column(Integer,ForeignKey("users.user_id"))

    cart_created_at = Column(DateTime,server_default=func.now())
    cart_updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())

    user_rel = relationship("User",back_populates="cart_rel")
    cart_item_rel = relationship("CartItem",back_populates="cart_rel")



class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True,autoincrement=True)

    cart_id = Column(Integer, ForeignKey("cart.cart_id"))

    product_id = Column(Integer, ForeignKey("product.product_id"))

    quantity = Column(Integer, default=1)

    cart_rel = relationship("Cart", back_populates="cart_item_rel")
    product_rel = relationship("Product", back_populates="cart_item_rel")