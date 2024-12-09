from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy.exc import IntegrityError
from api.models import Author, Book, Borrow
from db.database import get_db

app = FastAPI(
    title="API для управления библиотекой",
    description="Это API для управления авторами, книгами и заимствованиями.",
    version="1.0.0",
)

# Корневой эндпоинт
@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в API для управления библиотекой!"}

# Эндпоинт для добавления автора
@app.post("/authors/")
def add_author(first_name: str, last_name: str, birth_date: str, db: Session = Depends(get_db)):
    try:
        birth_date_obj = date.fromisoformat(birth_date)  # Преобразуем строку в дату
        new_author = Author(first_name=first_name, last_name=last_name, birth_date=birth_date_obj)
        db.add(new_author)
        db.commit()
        return {"message": f"Автор {first_name} {last_name} добавлен в базу данных."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка добавления автора в базу данных.")

# Эндпоинт для добавления книги
@app.post("/books/")
def add_book(title: str, description: str, author_id: int, available_copies: int, db: Session = Depends(get_db)):
    try:
        new_book = Book(title=title, description=description, author_id=author_id, available_copies=available_copies)
        db.add(new_book)
        db.commit()
        return {"message": f"Книга '{title}' добавлена в базу данных."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка добавления книги в базу данных.")

# Эндпоинт для записи о займе
@app.post("/borrows/")
def add_borrow(book_id: int, borrower_name: str, borrow_date: str, db: Session = Depends(get_db)):
    try:
        borrow_date_obj = date.fromisoformat(borrow_date)  # Преобразуем строку в дату
        book = db.query(Book).filter(Book.id == book_id, Book.available_copies > 0).first()
        if not book:
            raise HTTPException(status_code=404, detail="Книга не найдена или нет доступных копий.")

        new_borrow = Borrow(book_id=book.id, borrower_name=borrower_name, borrow_date=borrow_date_obj)
        db.add(new_borrow)
        book.available_copies -= 1  # Уменьшаем количество доступных копий
        db.commit()
        return {"message": f"Книга '{book.title}' была взята в заем {borrower_name} на {borrow_date}."}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ошибка при оформлении займа для книги.")
