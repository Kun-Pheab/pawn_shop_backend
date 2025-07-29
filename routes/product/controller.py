from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
# from models import Account
from database import get_db
from response_model import ResponseModel
from routes.oauth2.repository import get_current_user
from routes.product.repository import Staff
from routes.product.model import *
# from routes.user.model import CreatePawn 

router = APIRouter(
    tags=["Products"],
    # prefix="/api"
)

staff = Staff()
staff_service = Staff()

""" Product Management """
@router.post("/product", response_model = ResponseModel)
def create_product(product_info: CreateProduct, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    staff.is_staff(current_user)
    return staff.create_product(product_info, db, current_user)

@router.get("/product", response_model=ResponseModel)
def get_all_product(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page (max 100)"),
    search: Optional[str] = Query(None, description="Search products by name")
):
    staff.is_staff(current_user)
    return staff.get_product(db=db, page=page, limit=limit, search=search)

@router.get("/product/search", response_model=ResponseModel)
def search_products(
    search_term: str = Query(..., min_length=1, description="Search term for product name"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page (max 100)")
):
    """
    Search products by name with pagination
    """
    staff.is_staff(current_user)
    return staff.search_products(db=db, search_term=search_term, page=page, limit=limit)

@router.put("/product", response_model=ResponseModel)
def update_product(
    updated_product: UpdateProduct, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    staff_service = Staff()
    staff_service.is_staff(current_user)  

    return staff_service.update_product(
        db,
        prod_id=updated_product.prod_id,
        prod_name=updated_product.prod_name,
        unit_price=updated_product.unit_price,
        amount=updated_product.amount
    )

@router.delete("/product/{product_id}")
def delete_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_product_by_id(product_id, db)