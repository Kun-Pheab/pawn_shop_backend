from fastapi import HTTPException
from routes.user.model import *
from sqlalchemy.orm import Session
from entities import *
from response_model import ResponseModel
from typing import List, Dict
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
            
    def create_client(self, client_info: CreateClient, db: Session, not_exist: bool = False):
        existing_client = db.query(Account).filter(Account.phone_number == client_info.phone_number).first()
        if existing_client:
            raise HTTPException(
                status_code=400,
                detail="Phone Number already registered",
            )
        
        if not_exist:
            try:
                client = Account(
                    cus_name = client_info.cus_name, 
                    address = client_info.address,
                    phone_number = client_info.phone_number,)
                db.add(client)
                db.commit()
                db.refresh(client)
            except SQLAlchemyError as e:
                db.rollback()
                print(f"Error occurred: {str(e)}")
                raise HTTPException(status_code=500, detail="Database error occurred.")
            
            return client
            
        client = Account(
            cus_name = client_info.cus_name, 
            address = client_info.address,
            phone_number = client_info.phone_number,)
        
        db.add(client)
        db.commit()
        db.refresh(client)
        
        return ResponseModel(
            code=200,
            status="Success",
            message="Client created successfully"
        )
        
    def get_clients_paginated(self, page: int, db: Session, search: str = None, page_size: int = 10):
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Build base query
        query = db.query(Account).filter(Account.role == 'user')
        
        # Add search filters if search term is provided
        if search and search.strip():
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Account.cus_name.ilike(search_term),
                    Account.phone_number.ilike(search_term),
                    Account.address.ilike(search_term)
                )
            )
        
        # Get total count for pagination info
        total_clients = query.count()
        
        # Get paginated clients
        clients = query.offset(offset).limit(page_size).all()
        
        # Calculate pagination metadata
        total_pages = math.ceil(total_clients / page_size) if total_clients > 0 else 1
        has_next = page < total_pages
        has_previous = page > 1
        
        # Build response message
        message = "Clients retrieved successfully"
        if search and search.strip():
            message = f"Search results for '{search}' retrieved successfully"
            if total_clients == 0:
                message = f"No clients found matching '{search}'"
        
        return ResponseModel(
            code=200,
            status="Success",
            result=clients,
            message=message,
            pagination={
                "current_page": page,
                "page_size": page_size,
                "total_items": total_clients,
                "total_pages": total_pages,
                "has_next": has_next,
                "has_previous": has_previous,
                "search_term": search if search else None
            }
        )
        
    def get_client_phone(self, phone_number: str, db: Session):
        client = db.query(Account).filter(Account.phone_number == phone_number).all()
        
        if not client:
            # Return a structured response instead of raising an exception
            return ResponseModel(
                code=404,
                status="Not Found",
                result=[],
                message="Client not found"
            )
        
        return ResponseModel(
            code=200,
            status="Success",
            result=client
        )