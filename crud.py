from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc
from datetime import datetime
import models
import schemas

# Book CRUD
def get_books(db: Session, skip: int = 0, limit: int = 100, query: str = None, sort_by: str = None):
    q = db.query(models.Book)
    if query:
        search_filters = [
            models.Book.title.contains(query),
            models.Book.author.contains(query),
            models.Book.isbn.contains(query)
        ]
        try:
            query_as_int = int(query)
            search_filters.append(models.Book.id == query_as_int)
        except ValueError:
            pass
        
        q = q.filter(or_(*search_filters))
    if sort_by == 'title':
        q = q.order_by(asc(models.Book.title))
    elif sort_by == 'author':
        q = q.order_by(asc(models.Book.author))
    elif sort_by == 'available':
        q = q.order_by(desc(models.Book.available))
        
    return q.offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def toggle_book_availability(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        return None
    db_book.available = not db_book.available
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# User CRUD
def get_users(db: Session, skip: int = 0, limit: int = 100, query: str = None, sort_by: str = None):
    q = db.query(models.User)
    if query:
        search_filters = [
            models.User.name.contains(query),
            models.User.email.contains(query)
        ]
        try:
            query_as_int = int(query)
            search_filters.append(models.User.id == query_as_int)
        except ValueError:
            pass
        q = q.filter(or_(*search_filters))
    if sort_by == 'name':
        q = q.order_by(asc(models.User.name))
    return q.offset(skip).limit(limit).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# Transaction (Issue / Return)
def issue_book(db: Session, transaction: schemas.TransactionCreate):
    db_book = db.query(models.Book).filter(models.Book.id == transaction.book_id).first()
    if not db_book or not db_book.available:
        return None
    db_user = db.query(models.User).filter(models.User.id == transaction.user_id).first()
    if not db_user:
        return None
    
    db_book.available = False
    db_transaction = models.Transaction(**transaction.model_dump(), status="borrowed")
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def return_book(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction and db_transaction.status == "borrowed":
        db_transaction.status = "returned"
        db_book = db.query(models.Book).filter(models.Book.id == db_transaction.book_id).first()
        if db_book:
            db_book.available = True
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    return None

def get_transactions(db: Session, skip: int = 0, limit: int = 100, query: str = None):
    q = db.query(models.Transaction)
    if query:
        search_filters = [
            models.Transaction.status.contains(query)
        ]
        try:
            query_as_int = int(query)
            search_filters.extend([
                models.Transaction.id == query_as_int,
                models.Transaction.user_id == query_as_int,
                models.Transaction.book_id == query_as_int
            ])
        except ValueError:
            pass
        q = q.filter(or_(*search_filters))
    return q.offset(skip).limit(limit).all()

# New function for user transaction history
def get_user_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

# Add this new function to crud.py
def get_user_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()

