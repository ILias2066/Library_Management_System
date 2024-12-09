from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models import Book, Author
from db.database import get_db

router = APIRouter()

@router.post("/books", response_model=dict)
def create_book(title: str, description: str, author_id: int, available_copies: int, db: Session = Depends(get_db)):
    author = db.query(Author).get(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    book = Book(title=title, description=description, author_id=author_id, available_copies=available_copies)
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"id": book.id}

@router.get("/books")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{book_id}")
def update_book(book_id: int, title: str, description: str, available_copies: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = title
    book.description = description
    book.available_copies = available_copies
    db.commit()
    return {"message": "Book updated"}

@router.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}
