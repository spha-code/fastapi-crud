from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base
from schemas import Item, ItemCreate
from crud import get_items, get_item, create_item, update_item, delete_item

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple CRUD API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Serve static files and frontend
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")

# API endpoints
@app.get("/api/items", response_model=list[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_items(db, skip=skip, limit=limit)

@app.post("/api/items", response_model=Item)
def create_new_item(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db=db, item=item)

@app.get("/api/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/api/items/{item_id}", response_model=Item)
def update_existing_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = update_item(db, item_id=item_id, item_data=item.model_dump())
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/api/items/{item_id}")
def delete_existing_item(item_id: int, db: Session = Depends(get_db)):
    db_item = delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}