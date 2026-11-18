from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel,Field
from typing import Optional

from starlette import status

app = FastAPI()


#Data Validation
class Book:
    id: int
    title: str
    author: str
    description: str
    published_date: int
    rating: int

    def __init__(self,id,title,author, description,published_date, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.published_date  = published_date
        self.rating = rating





class Book_Request(BaseModel):
    id: Optional[int] = Field(title="ID is not needed", default = None)
    title: str = Field(min_length = 3, max_length = 50)
    author: str = Field(min_length = 3, max_length = 100)
    description: str = Field(min_length = 3, max_length = 100)
    published_date: int = Field(min_digits=4)
    rating: int = Field(gt=0, lt=6)


    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Eshwar",
                "description": "A new description of a book",
                "published_date": 2012,
                "rating": 5        
            }
        }
    }

#Data validation ends



BOOKS = [
    Book(1,"Title One","eshwar","Great Movie",2000,4),
    Book(2,"Title One","eshwar","Great Movie",2005,5),
    Book(3,"Title One","eshwar","Great Movie",2010,3),
    Book(4,"Title One","eshwar","Great Movie",2020,2)
]



#Read all books
@app.get("/books", status_code = status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


#Read book by id
@app.get("/books/{book_id}", status_code = status.HTTP_200_OK)
async def read_book_by_id(book_id:int = Path(gt = 0)):#path parameter validation
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code = 404, detail = "Item not Found")


#Read Book by Rating
@app.get("/books/", status_code = status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int =Query(gt=0, lt = 6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return 

#Read books by date
@app.get("/books/publish/", status_code = status.HTTP_200_OK)
async def read_book_by_date(book_date: int = Query(gt = 1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == book_date:
            books_to_return.append(book)
    return books_to_return 

        

@app.post("/create-book", status_code = status.HTTP_201_CREATED)
async def create_book(book_request: Book_Request):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    
    book.id = 1 if len(BOOKS)==0 else BOOKS[-1].id+1
    # if len(BOOKS)>0:
    #    book.id = BOOKS[-1].id+1
    # else:
    #    book.id = 1
    return book


@app.put("/books/update-book", status_code = status.HTTP_204_NO_CONTENT)
async def update_book(book: Book_Request):
    book_changed = False
    for i in range(len(BOOKS)):
        if book.id == BOOKS[i].id:
            BOOKS[i] = book
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code = 404, detail = "Item not Found")


@app.delete("/books/delete-book/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_by_id(book_id:int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code = 404, detail = "Item not Found")

