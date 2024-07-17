from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items = {}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the sample API"}

@app.get("/items")
async def read_items():
    return items

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@app.post("/items")
async def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, **item.dict()}

@app.get("/slow")
async def slow_response():
    time.sleep(2)  # Simulate a slow response
    return {"message": "This was a slow response"}