from fastapi import APIRouter, FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import BookSchema, Book, Token
from auth import authenticate_user, create_access_token, get_current_user
import crud
from sse import get_stream, broadcast_update
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Books API with SQLAlchemy", version="1.0")


@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


protected_router = APIRouter(dependencies=[Depends(get_current_user)])


@protected_router.post("/books/", response_model=Book)
def create(book: BookSchema, db: Session = Depends(get_db)):
    book_id = crud.create_book(db, book)
    broadcast_update(f"Book created: {book.title}")
    return crud.get_book(db, book_id)


@protected_router.get("/books/", response_model=list[Book])
def read_books(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, gt=0),
    db: Session = Depends(get_db),
):
    return crud.get_books(db, skip, limit)


@protected_router.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    return crud.get_book(db, book_id)


@protected_router.put("/books/{book_id}", response_model=Book)
def update(book_id: int, book: BookSchema, db: Session = Depends(get_db)):
    crud.update_book(db, book_id, book)
    broadcast_update(f"Book updated: {book.title}")
    return crud.get_book(db, book_id)


@protected_router.delete("/books/{book_id}", status_code=204)
def delete(book_id: int, db: Session = Depends(get_db)):
    crud.delete_book(db, book_id)
    broadcast_update(f"Book deleted ID: {book_id}")
    return


@protected_router.get("/stream")
def stream():
    return get_stream()


app.include_router(protected_router)
