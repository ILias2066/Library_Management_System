from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from db.database import get_db
from api.models import Author, Book, Borrow

router = APIRouter()

# Маршрут для добавления автора
@router.post("/authors")
def add_author(first_name: str, last_name: str, birth_date: date, db: Session = Depends(get_db)):
    new_author = Author(first_name=first_name, last_name=last_name, birth_date=birth_date)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return {"message": f"Автор {first_name} {last_name} добавлен."}

# Маршрут для добавления книги
@router.post("/books")
def add_book(title: str, description: str, author_id: int, available_copies: int, db: Session = Depends(get_db)):
    new_book = Book(title=title, description=description, author_id=author_id, available_copies=available_copies)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message": f"Книга '{title}' добавлена."}

# Маршрут для добавления записи о заимствовании
@router.post("/borrows")
def add_borrow(book_id: int, borrower_name: str, borrow_date: date, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id, Book.available_copies > 0).first()
    if not book:
        return {"message": "Книга недоступна для заимствования."}

    new_borrow = Borrow(book_id=book_id, borrower_name=borrower_name, borrow_date=borrow_date)
    db.add(new_borrow)
    book.available_copies -= 1
    db.commit()
    db.refresh(new_borrow)
    return {"message": f"Книга '{book.title}' была заимствована {borrower_name}."}
