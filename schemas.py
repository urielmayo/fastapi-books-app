from datetime import date
from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BookSchema(BaseModel):
    title: str
    author: str
    published_date: date
    summary: str
    genre: str


class Book(BookSchema):
    id: int

    class Config:
        orm_mode = True
