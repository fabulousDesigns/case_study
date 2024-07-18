from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)  # New field
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    item = Column(String)
    amount = Column(Float)
    time = Column(DateTime)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="orders")