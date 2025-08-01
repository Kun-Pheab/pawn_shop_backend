from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from response_model import ResponseModel
from routes.oauth2.repository import get_current_user
from routes.order.repository import Staff
from routes.order.model import *

router = APIRouter(
    tags=["Orders"],
    # prefix="/api"
)

staff = Staff()
staff_service = Staff()

""" Manage Order and Payment """
@router.post("/order", response_model = ResponseModel)
def create_order(order_info: CreateOrder, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    staff.is_staff(current_user)
    return staff.create_order(order_info, db, current_user)

@router.get("/order", response_model=ResponseModel)
def get_client_order(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.get_client_order(db)

@router.get("/order/all_client", response_model=ResponseModel)
def get_all_client_order(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page (1-100)"),
    search_id: int = Query(None, description="Search by customer ID"),
    search_name: str = Query(None, description="Search by customer name"),
    search_phone: str = Query(None, description="Search by phone number"),
    search_address: str = Query(None, description="Search by address"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    
    # Additional validation to prevent the error
    if search_id is not None:
        try:
            # Ensure it's a valid integer
            search_id = int(search_id)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid ID format. ID must be a valid integer, received: {search_id}"
            )
    
    return staff.get_all_client_order_paginated(page, db, search_id, search_name, search_phone, search_address, limit)

@router.get("/order/client/{cus_id}", response_model=ResponseModel)
def get_client_id(
    cus_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.get_client_id(cus_id, db)

@router.get("/order/search", response_model=ResponseModel)
def get_client_order(
    phone_number: Optional[str] = None,
    cus_name: Optional[str] = None,
    cus_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.get_client_order(db, phone_number, cus_name, cus_id)

@router.get("/order/next-id", response_model=ResponseModel)
def get_next_order_id(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.get_next_order_id(db)

@router.get("/order/last", response_model=ResponseModel)
def get_last_order(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.get_last_order(db)

@router.get("/order/print", response_model=ResponseModel)
def get_order_print(
    order_id: Optional[int] = None, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)):

    staff.is_staff(current_user) 
    if not order_id:
        raise HTTPException(status_code=400, detail="Order ID is required")
    
    try:
        # Call your staff.get_order_print function
        result = staff.get_order_print(db, order_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/order/{order_id}", response_model=ResponseModel)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_order(order_id, db)

@router.patch("/order/{order_id}", response_model=ResponseModel)
def update_order(
    order_id: int,
    order_update: PatchOrder,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.update_order(order_id, order_update, db, current_user)