from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List


# Define a model for the item
class Item(BaseModel):
    name: str
    price: float
    description: str = None

# Create an instance of the FastAPI class
app = FastAPI()

# Create an in-memory database to store items
db: Dict[int, Item] = {}

# Counter to keep track of item IDs
item_id_counter = 1

# Route to create a new item
@app.post("/items/")
async def create_item(item: Item):
    global item_id_counter
    db[item_id_counter] = item
    item_id_counter += 1
    return item

# Route to retrieve an item by ID
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    return db[item_id]

# Route to update an item by ID
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item
    return {"message": "Item updated successfully"}

# Route to delete an item by ID
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message": "Item deleted successfully"}

# Route to retrieve all items
@app.get("/items/")
async def read_all_items():
    return [{"id": k, **v.dict()} for k, v in db.items()]
