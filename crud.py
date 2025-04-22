from typing import List
from sqlalchemy.orm import Session
from models import Book
from schemas import BookCreate, BookPartialUpdate, BookUpdate
from fastapi import HTTPException


def create_book(db: Session, book: BookCreate) -> int:
    db_book = Book(**dict(book))
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book.id  # type: ignore


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Book:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate) -> Book:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in book.model_dump().items():
        setattr(db_book, field, value)
    db.commit()
    return db_book


def partial_update_book(
    db: Session, book_id: int, book: BookPartialUpdate
) -> Book:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in book.model_dump(exclude_none=True).items():
        setattr(db_book, field, value)
    db.commit()
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
