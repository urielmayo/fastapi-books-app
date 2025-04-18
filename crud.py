from typing import List
from sqlalchemy.orm import Session
from models import Book
from schemas import BookSchema
from fastapi import HTTPException


def create_book(db: Session, book: BookSchema) -> int:
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


def update_book(db: Session, book_id: int, book: BookSchema) -> Book:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in book.model_dump().items():
        setattr(db_book, field, value)
    db.commit()
    return db_book


def delete_book(db: Session, book_id: int) -> None:
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
