from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Book Schema
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    available: bool

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2

# User Schema
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2

# Transaction Schema
class TransactionBase(BaseModel):
    user_id: int
    book_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    status: str
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2

# Add these new schemas to schemas.py

# Book Schema for Updates
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None

# User Schema for Updates
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class TransactionBase(BaseModel):
    user_id: int
    book_id: int

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    status: str
    timestamp: Optional[datetime] = None
    due_date: Optional[datetime] = None # Add this line

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2

