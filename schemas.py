from datetime import date
from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BookSchema(BaseModel):
    title: str = Field(description="Book title")
    author: str = Field(description="Author name")
    published_date: date = Field(description="Published date")
    summary: str = Field(description="Short summary of the book")
    genre: str = Field(description="Book genre")


class BookCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Book title",
    )
    author: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Author name",
    )
    published_date: date = Field(..., description="Published date")
    summary: str = Field(
        ...,
        max_length=1000,
        description="Short summary of the book",
    )
    genre: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Book genre",
    )


class BookUpdate(BookCreate):
    pass


class BookPartialUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Book title",
    )
    author: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Author name",
    )
    published_date: date | None = Field(
        default=None,
        description="Published date",
    )
    summary: str | None = Field(
        default=None,
        max_length=1000,
        description="Short summary of the book",
    )
    genre: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
        description="Book genre",
    )


class BookRead(BookSchema):
    id: int

    class Config:
        orm_mode = True
