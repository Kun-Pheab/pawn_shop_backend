from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
# from models import Account
from database import get_db
from response_model import ResponseModel
from routes.oauth2.repository import get_current_user
from routes.user.repository import Staff
from routes.user.model import *
# from routes.user.model import CreatePawn 

router = APIRouter(
    tags=["Other"],
    prefix="/noe"
)

staff = Staff()
staff_service = Staff()


@router.get("/orders/print", response_model=ResponseModel)
def get_order_by_id(order_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve all orders or a specific order by ID along with customer details.
    """
    return staff.get_order_by_id(db, order_id)

@router.get("/pawn/print", response_model=ResponseModel)
def get_pawn_by_id(pawn_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Retrieve all orders or a specific order by ID along with customer details.
    """
    return staff.get_pawn_by_id(db, pawn_id)

"""Delete product by ID"""
@router.delete("/products/{product_id}")
def delete_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_product_by_id(product_id, db)

"""Delete product by name"""
@router.delete("/products/name/{product_name}")
def delete_product_by_name(
    product_name: str, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_product_by_name(product_name, db)

"""Delete all products"""
@router.delete("/products")
def delete_all_products(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_all_products(db)

@router.get("/products/search/{search_input}", response_model=ResponseModel)
def search_product(
    search_input: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    staff.is_staff(current_user)
    try:
        if search_input.isdigit():
            product = staff.get_product_by_id(int(search_input), db)
            return ResponseModel(
                code=200,
                status="success",
                message="Product retrieved successfully",
                result=product,
            )
        else:
            products = staff.get_product_by_name(search_input, db)
            return ResponseModel(
                code=200,
                status="success",
                message="Products retrieved successfully",
                result=products,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

"""Delete product by ID"""
@router.delete("/products/{product_id}")
def delete_product_by_id(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_product_by_id(product_id, db)

"""Delete product by name"""
@router.delete("/products/name/{product_name}")
def delete_product_by_name(
    product_name: str, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_product_by_name(product_name, db)

"""Delete all products"""
@router.delete("/products")
def delete_all_products(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)
    return staff.delete_all_products(db)

@router.get("/products/search/{search_input}", response_model=ResponseModel)
def search_product(
    search_input: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    staff.is_staff(current_user)
    try:
        if search_input.isdigit():
            product = staff.get_product_by_id(int(search_input), db)
            return ResponseModel(
                code=200,
                status="success",
                message="Product retrieved successfully",
                result=product,
            )
        else:
            products = staff.get_product_by_name(search_input, db)
            return ResponseModel(
                code=200,
                status="success",
                message="Products retrieved successfully",
                result=products,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


""" Retrieve Next Product ID """
@router.get("/next-product-id", response_model=ResponseModel)
def get_next_product_id(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)  # Ensure authorization
    response = staff.get_next_product_id(db)

    return ResponseModel(
        code=200,
        status="success",
        message="Next product ID retrieved successfully",
        result=response["result"]
    )


""" Retrieve Next Client ID """
@router.get("/next-client-id", response_model=ResponseModel)
def get_next_client_id(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)  # Ensure authorization
    response = staff.get_next_client_id(db)

    return ResponseModel(
        code=200,
        status="success",
        message="Next client ID retrieved successfully",
        result=response["result"]
    )


""" Retrieve Next Order ID """
@router.get("/next-order-id", response_model=ResponseModel)
def get_next_order_id(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)  # Ensure authorization
    response = staff.get_next_order_id(db)

    return ResponseModel(
        code=200,
        status="success",
        message="Next order ID retrieved successfully",
        result=response["result"]
    )


""" Retrieve Next Pawn ID """
@router.get("/next-pawn-id", response_model=ResponseModel)
def get_next_pawn_id(
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    staff.is_staff(current_user)  # Ensure authorization
    response = staff.get_next_pawn_id(db)

    return ResponseModel(
        code=200,
        status="success",
        message="Next pawn ID retrieved successfully",
        result=response["result"]
    )
    

@router.put("/product", response_model=ResponseModel)
def update_product(
    updated_product: UpdateProduct,  # Accept JSON as request body
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    staff_service = Staff()
    staff_service.is_staff(current_user)  # Ensure user is staff/admin

    return staff_service.update_product(
        db,
        prod_id=updated_product.prod_id,
        prod_name=updated_product.prod_name,
        unit_price=updated_product.unit_price,
        amount=updated_product.amount
    )
