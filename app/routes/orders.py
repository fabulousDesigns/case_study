from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.utils.sms_sender import send_sms
from app.utils.utils import VerifyToken

from ..models.models import Customer, Order

router = APIRouter()
verify_token = VerifyToken()

class OrderCreate(BaseModel):
    customer_id: int
    item: str
    amount: float
    time: datetime

class OrderUpdate(BaseModel):
    item: str
    amount: float
    time: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders", dependencies=[Depends(verify_token.verify)], tags=["orders"])
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    db_order = Order(
        customer_id=order.customer_id,
        item=order.item,
        amount=order.amount,
        time=order.time
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    message = f"New order placed: {order.item} for ${order.amount:.2f}"
    sms_response = send_sms(str(db_customer.phone_number), message)  # Convert to string

    return {"order": db_order, "sms_response": sms_response}

@router.get("/orders", dependencies=[Depends(verify_token.verify)], tags=["orders"])
async def get_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders

@router.get("/orders/{order_id}", dependencies=[Depends(verify_token.verify)], tags=["orders"])
async def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/orders/{order_id}", dependencies=[Depends(verify_token.verify)], tags=["orders"])
async def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    for key, value in order.dict().items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/orders/{order_id}", dependencies=[Depends(verify_token.verify)], tags=["orders"])
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": "Order deleted successfully"}