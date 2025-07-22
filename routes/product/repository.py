from fastapi import HTTPException
from routes.user.model import *
from sqlalchemy.orm import Session
from entities import *
from response_model import ResponseModel
from typing import List, Dict, Optional
# from app.models import Client, Pawn
from sqlalchemy.sql import func, or_, and_
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
from typing import Dict, Any
import math

class Staff:
    def is_staff(self, current_user: dict):
        if current_user['role'] != 'admin':
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )
            
    # ========== Create New Product ==========
    def create_product(self, product_info: CreateProduct, db: Session, current_user: dict):
            existing_product = db.query(Product).filter(Product.prod_name == func.lower(product_info.prod_name)).first()
            if existing_product:
                raise HTTPException(
                    status_code=400,
                    detail="Product already exists",
                )
                
            if product_info.amount != None and product_info.unit_price != None:
                product = Product(
                    prod_name = func.lower(product_info.prod_name),
                    unit_price = product_info.unit_price,
                    amount = product_info.amount,
                    user_id = current_user['id'])
                db.add(product)
                db.commit()
                db.refresh(product)
                
            else: 
                product = Product(prod_name = func.lower(product_info.prod_name), user_id = current_user['id'])
                db.add(product)
                db.commit()
                db.refresh(product)
                return product
            
            
            return ResponseModel(
                code=200,
                status="Success",
                message="Product created successfully"
            )
            
    # ========== Get All Products with Pagination and Search ==========
    def get_product(self, db: Session, page: int = 1, limit: int = 10, search: Optional[str] = None):
        # Calculate offset for pagination
        offset = (page - 1) * limit
        
        # Base query
        query = db.query(Product)
        
        # Add search filter if provided
        if search:
            search_filter = or_(
                Product.prod_name.ilike(f"%{search}%"),
                # You can add more fields to search in if needed
                # Product.description.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        # Get total count for pagination info
        total_count = query.count()
        
        # Apply pagination
        products = query.offset(offset).limit(limit).all()
        
        if not products and page > 1:
            raise HTTPException(
                status_code=404,
                detail="No products found on this page",
            )
        
        # Calculate pagination info
        total_pages = math.ceil(total_count / limit) if total_count > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1
        
        serialized_products = [
            {
                "id": product.prod_id,
                "name": product.prod_name,
                "price": product.unit_price,
                "amount": product.amount,
            }
            for product in products
        ]
        
        return ResponseModel(
            code=200,
            status="Success",
            result={
                "products": serialized_products,
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_count": total_count,
                    "limit": limit,
                    "has_next": has_next,
                    "has_prev": has_prev
                }
            }
        )
    
    # ========== Search Products ==========
    def search_products(self, db: Session, search_term: str, page: int = 1, limit: int = 10):
        """
        Search products by name with pagination
        """
        if not search_term.strip():
            raise HTTPException(
                status_code=400,
                detail="Search term cannot be empty"
            )
        
        # Calculate offset
        offset = (page - 1) * limit
        
        # Search query
        search_filter = Product.prod_name.ilike(f"%{search_term}%")
        
        # Get total count
        total_count = db.query(Product).filter(search_filter).count()
        
        # Get products with pagination
        products = db.query(Product).filter(search_filter).offset(offset).limit(limit).all()
        
        if not products:
            return ResponseModel(
                code=200,
                status="Success",
                result={
                    "products": [],
                    "pagination": {
                        "current_page": page,
                        "total_pages": 0,
                        "total_count": 0,
                        "limit": limit,
                        "has_next": False,
                        "has_prev": False
                    }
                },
                message="No products found matching your search"
            )
        
        # Calculate pagination info
        total_pages = math.ceil(total_count / limit)
        has_next = page < total_pages
        has_prev = page > 1
        
        serialized_products = [
            {
                "id": product.prod_id,
                "name": product.prod_name,
                "price": product.unit_price,
                "amount": product.amount,
            }
            for product in products
        ]
        
        return ResponseModel(
            code=200,
            status="Success",
            result={
                "products": serialized_products,
                "pagination": {
                    "current_page": page,
                    "total_pages": total_pages,
                    "total_count": total_count,
                    "limit": limit,
                    "has_next": has_next,
                    "has_prev": has_prev
                }
            },
            message=f"Found {total_count} products matching '{search_term}'"
        )
        
    # ========== Update Existing Product ==========
    def update_product(
        self,
        db: Session,
        prod_id: Optional[int] = None,
        prod_name: Optional[str] = None,
        unit_price: Optional[float] = None,
        amount: Optional[int] = None,
    ):
        if not prod_id and not prod_name:
            raise HTTPException(
                status_code=400,
                detail="Product ID or Name is required to update the product.",
            )

        # Search for product by ID or Name
        product_query = db.query(Product)
        if prod_id:
            product_query = product_query.filter(Product.prod_id == prod_id)
        elif prod_name:
            product_query = product_query.filter(Product.prod_name.ilike(prod_name))

        product = product_query.first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found.",
            )

        # Update only amount and price if provided
        if unit_price is not None:
            product.unit_price = unit_price
        if amount is not None:
            product.amount = amount

        db.commit()
        db.refresh(product)

        return ResponseModel(
            code=200,
            status="Success",
            message="Product updated successfully",
            result={
                "id": product.prod_id,
                "name": product.prod_name,
                "price": product.unit_price,
                "amount": product.amount,
            }
        )

    # ========== Delete Product ==========
    def delete_product_by_id(self, product_id: int, db: Session):
        """
        Deletes a product by its ID.
        """
        product = db.query(Product).filter(Product.prod_id == product_id).first()
        if not product:
            # Instead of raising an exception, return a success message
            return ResponseModel(
                code=200,
                status="Success",
                message=f"Product with ID {product_id} not found but considered deleted"
            )

        try:
            db.delete(product)
            db.commit()
            return ResponseModel(
                code=200,
                status="Success",
                message=f"Product with ID {product_id} deleted successfully"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Database error occurred: {str(e)}",
            )