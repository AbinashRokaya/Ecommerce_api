from sqlalchemy import Column,String,Integer,ForeignKey,DECIMAL,DateTime
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer,primary_key=True,autoincrement=True)
    order_amount = Column(DECIMAL)
    order_user_id = Column(Integer,ForeignKey("users.user_id"))

    order_created_at = Column(DateTime,server_default=func.now())
    order_user_updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now())

    user_rel = relationship("User",back_populates="order_rel")
    # cart_rel = relationship("Cart",back_populates="order_rel")
    payment_rel = relationship("Payment",back_populates="order_rel")
    order_item_rel = relationship("OrderItem",back_populates="order_rel")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True,autoincrement=True)

    order_id = Column(Integer, ForeignKey("order.order_id"))

    product_id = Column(Integer, ForeignKey("product.product_id"))

    quantity = Column(Integer)

    price = Column(DECIMAL)

    order_rel = relationship("Order", back_populates="order_item_rel")

    product_rel = relationship("Product", back_populates="order_item_rel")

