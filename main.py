from models import Books
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get-book/{book_name}")
async def getBook(book_name: Books):
    if book_name.value == "book1":
        return {"book": Books.book1}

    if book_name is Books.book2:
        return {"book": Books.book2}

    if book_name.value == "book3":
        return {"book": Books.book3}

