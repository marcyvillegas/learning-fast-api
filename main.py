from typing import Annotated
from fastapi import FastAPI, Query, Path, Body
from models import Books, Item, User

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

@app.get("/items/")
async def getItems(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}, {"item_id": "Sample1"}, {"item_id": "SAmple2"}, {"item_id": "SAmple3"}]}
    if q:
        results.update({"query": q})
    return results

"""
Result:
{
  "items": [
    {
      "item_id": "Foo"
    },
    {
      "item_id": "Bar"
    },
    {
      "item_id": "Sample1"
    },
    {
      "item_id": "SAmple2"
    },
    {
      "item_id": "SAmple3"
    }
  ],
  "q": "dasf"
}
"""

@app.get("/search-item/")
async def searchItems(q: Annotated[str | None, Query(alias="search")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"searchKeyword": q})
    return results

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

@app.put("/items/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results