from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.models import Borrow, Book
from db.database import get_db

router = APIRouter()

@router.post("/borrows", response_model=dict)
def create_borrow(book_id: int, borrower_name: str, borrow_date: str, db: Session = Depends(get_db)):
    book = db.query(Book).get(book_id)
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")
    borrow = Borrow(book_id=book_id, borrower_name=borrower_name, borrow_date=borrow_date)
    book.available_copies -= 1
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return {"id": borrow.id}

@router.get("/borrows")
def get_borrows(db: Session = Depends(get_db)):
    return db.query(Borrow).all()

@router.get("/borrows/{borrow_id}")
def get_borrow(borrow_id: int, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).get(borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow not found")
    return borrow

@router.patch("/borrows/{borrow_id}/return")
def return_borrow(borrow_id: int, return_date: str, db: Session = Depends(get_db)):
    borrow = db.query(Borrow).get(borrow_id)
    if not borrow or borrow.return_date:
        raise HTTPException(status_code=400, detail="Borrow already returned or not found")
    borrow.return_date = return_date
    book = db.query(Book).get(borrow.book_id)
    book.available_copies += 1
    db.commit()
    return {"message": "Book returned"}
