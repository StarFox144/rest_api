from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

app = FastAPI()

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    created_at: Optional[datetime] = None

items_db = []
current_id = 1

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    global current_id
    item.id = current_id
    item.created_at = datetime.now()
    items_db.append(item)
    current_id += 1
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, updated_item: Item):
    item_idx = next((idx for idx, item in enumerate(items_db) if item.id == item_id), None)
    if item_idx is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item.id = item_id
    updated_item.created_at = items_db[item_idx].created_at
    items_db[item_idx] = updated_item
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    item_idx = next((idx for idx, item in enumerate(items_db) if item.id == item_id), None)
    if item_idx is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    items_db.pop(item_idx)
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
