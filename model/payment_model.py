from sqlalchemy import Column,String,Integer,ForeignKey,Enum,DateTime,DECIMAL
from database.database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from enum_schema.payment_enum import PaymentType,PaymentStatus


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer,primary_key=True,autoincrement=True)
    payment_order_id = Column(Integer,ForeignKey("order.order_id"))
    payment_user_id = Column(Integer,ForeignKey("users.user_id"))
    payment_type = Column(Enum(PaymentType), 
        default=PaymentType.CREDIT_CARD, 
        nullable=False)
    
    payment_method = Column(String)
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_transaction_id = Column(String)
    payment_amount = Column(DECIMAL)
    payment_created_at = Column(DateTime,server_default=func.now())

    user_rel = relationship("User",back_populates="payment_rel")
    order_rel = relationship("Order",back_populates="payment_rel")
    