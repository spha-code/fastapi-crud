

touch main.py database.py models.py schemas.py crud.py
mkdir static
touch static/index.html static/app.js


# FastAPI CRUD Application with Plain JavaScript
A complete, production-ready CRUD application built with FastAPI, SQLAlchemy, SQLite, and vanilla JavaScript. No JavaScript frameworks or complex templating—just clean, simple code that's easy to understand and modify.

![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat&logo=javascript)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## ✨ Features
- Full CRUD operations (Create, Read, Update, Delete)
- RESTful API built with FastAPI
- SQLite database with SQLAlchemy ORM
- Vanilla JavaScript frontend (no frameworks!)
- Modern async/await JavaScript
- Responsive design with pure CSS
- Simple project structure
- Hot-reload development server
- Comprehensive error handling

## 📁 Final Project Structure
fastapi-crud/
├── pyproject.toml
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
└── static/
    ├── index.html
    ├── style.css
    └── app.js

## 🚀 Getting Started
### Prerequisites
- Python 3.8 or higher
- UV package manager

### Step 1: Install UV Package Manager
macOS / Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

### Step 2: Create Project Directory & Initialize
mkdir fastapi-crud
cd fastapi-crud
uv init

### Step 3: Install Dependencies
uv add fastapi uvicorn sqlalchemy

---

# 💾 Create the Application Files

## 1. database.py

        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        
        SQLALCHEMY_DATABASE_URL = "sqlite:///./items.db"
        
        engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

        Base = declarative_base()

## 2. models.py

        from sqlalchemy import Column, Integer, String, Boolean
        from database import Base
        
        class Item(Base):
            __tablename__ = "items"
        
            id = Column(Integer, primary_key=True, index=True)
            name = Column(String, index=True)
            description = Column(String)
            completed = Column(Boolean, default=False)

## 3. schemas.py
            
            from pydantic import BaseModel
            
            class ItemBase(BaseModel):
                name: str
                description: str | None = None
                completed: bool = False
            
            class ItemCreate(ItemBase):
                pass
            
            class Item(ItemBase):
                id: int
                class Config:
                    from_attributes = True
            
## 4. crud.py

            from sqlalchemy.orm import Session
            from models import Item as ItemModel
            from schemas import ItemCreate
            
            def get_items(db: Session, skip: int = 0, limit: int = 100):
                return db.query(ItemModel).offset(skip).limit(limit).all()
            
            def get_item(db: Session, item_id: int):
                return db.query(ItemModel).filter(ItemModel.id == item_id).first()
            
            def create_item(db: Session, item: ItemCreate):
                db_item = ItemModel(**item.model_dump())
                db.add(db_item)
                db.commit()
                db.refresh(db_item)
                return db_item
            
            def update_item(db: Session, item_id: int, item_data: dict):
                db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
                if db_item:
                    for key, value in item_data.items():
                        setattr(db_item, key, value)
                    db.commit()
                    db.refresh(db_item)
                return db_item
            
            def delete_item(db: Session, item_id: int):
                db_item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
                if db_item:
                    db.delete(db_item)
                    db.commit()
                return db_item

## 5. main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base
from schemas import Item, ItemCreate
from crud import get_items, get_item, create_item, update_item, delete_item

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple CRUD API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")

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

## 6. Static Files
### index.html
(HTML content exactly as provided)

### style.css
(CSS content exactly as provided)

### app.js
(JavaScript content exactly as provided)

---

## 🏃 Run the Application
cd ..
uv run uvicorn main:app --reload

Visit: http://localhost:8000

## 📡 API Endpoints
Method | Endpoint | Description
GET | /api/items | Get all items  
POST | /api/items | Create new item  
GET | /api/items/{id} | Get item  
PUT | /api/items/{id} | Update item  
DELETE | /api/items/{id} | Delete item  

Swagger UI: /docs  
ReDoc: /redoc  

## 🔧 Customization
- Change database in `database.py`
- Add new fields by editing model, schemas, frontend, JS
- Change port:
uv run uvicorn main:app --reload --port 9000

## 📖 What You Learned
- Setting up FastAPI with UV  
- SQLAlchemy models  
- Pydantic schemas  
- RESTful API development  
- Vanilla JS frontend  
- Fetch API usage  
- DOM manipulation  

## 🤝 Contributing
Fork, modify, and open PRs!

## 📄 License
MIT License

## 💡 Tips
- Use uv add instead of editing pyproject.toml  
- items.db is auto-created  
- Use /docs for API exploration  
- Use DevTools for JS debugging  
- Hot reload for rapid development  
