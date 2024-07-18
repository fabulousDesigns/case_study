from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.utils.utils import VerifyToken

from ..models.models import Customer

router = APIRouter()
verify_token = VerifyToken()

class CustomerCreate(BaseModel):
    name: str
    code: str
    phone_number: str

class CustomerUpdate(BaseModel):
    name: str
    code: str
    phone_number: str

class CustomerResponse(BaseModel):
    id: int
    name: str
    code: str
    phone_number: str

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/customers", response_model=CustomerResponse, dependencies=[Depends(verify_token.verify)], tags=["customers"])
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = Customer(name=customer.name, code=customer.code, phone_number=customer.phone_number)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.get("/customers", response_model=List[CustomerResponse], dependencies=[Depends(verify_token.verify)], tags=["customers"])
async def get_all_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers

@router.get("/customers/{customer_id}", response_model=CustomerResponse, dependencies=[Depends(verify_token.verify)], tags=["customers"])
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/customers/{customer_id}", response_model=CustomerResponse, dependencies=[Depends(verify_token.verify)], tags=["customers"])
async def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in customer.dict().items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

@router.delete("/customers/{customer_id}", dependencies=[Depends(verify_token.verify)], tags=["customers"])
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}