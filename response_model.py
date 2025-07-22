from typing import Optional, TypeVar, Generic, Dict, Any
from pydantic import BaseModel
T = TypeVar("T")

class ResponseModel(BaseModel, Generic[T]):
    code: int
    status: str
    message: Optional[str] = None
    result: Optional[T] = None
    pagination: Optional[Dict[str, Any]] = None