from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from typing import List
import crud

# Import your modules
import models
import schemas
import crud
import database

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# Create the FastAPI app
app = FastAPI(title="Library Management System", version="1.0.0")

# Optional: Mount static files if directory exists
static_dir = "static"
if os.path.exists(static_dir):
    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Optional: Set up templates if jinja2 is installed
templates = None
try:
    from fastapi.templating import Jinja2Templates
    from fastapi.responses import HTMLResponse
    from fastapi import Request
    
    templates_dir = "templates"
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    templates = Jinja2Templates(directory=templates_dir)
except ImportError:
    print("Jinja2 not installed. Template routes will be disabled.")
    print("Install with: pip install jinja2")
except Exception as e:
    print(f"Template setup failed: {e}")

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Homepage route (only if templates are available)
if templates:
    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
else:
    @app.get("/")
    async def read_root():
        return {
            "message": "Library Management System API",
            "docs": "/docs",
            "endpoints": {
                "books": "/books/",
                "users": "/users/",
                "transactions": "/transactions/"
            }
        }

# Book routes
@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 10, query: str = None, sort_by: str = None, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit, query=query, sort_by=sort_by)
    return books

@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated_book = crud.update_book(db=db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    if not crud.delete_book(db=db, book_id=book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

@app.put("/books/{book_id}/toggle-availability", response_model=schemas.Book)
def toggle_book_availability(book_id: int, db: Session = Depends(get_db)):
    updated_book = crud.toggle_book_availability(db=db, book_id=book_id)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

# User routes
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, query: str = None, sort_by: str = None, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit, query=query, sort_by=sort_by)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db=db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Transaction routes
@app.post("/transactions/issue/", response_model=schemas.Transaction)
def issue_book(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    result = crud.issue_book(db=db, transaction=transaction)
    if result is None:
        raise HTTPException(status_code=400, detail="Book not available or user/book not found")
    return result

@app.put("/transactions/{transaction_id}/return/", response_model=schemas.Transaction)
def return_book(transaction_id: int, db: Session = Depends(get_db)):
    result = crud.return_book(db=db, transaction_id=transaction_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Transaction not found or book already returned")
    return result

@app.get("/transactions/", response_model=list[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 10, query: str = None, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, skip=skip, limit=limit, query=query)
    return transactions

# Add this new route to main.py
@app.get("/users/{user_id}/transactions/", response_model=list[schemas.Transaction])
def read_user_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = crud.get_user_transactions(db=db, user_id=user_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="User or transactions not found")
    return transactions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)