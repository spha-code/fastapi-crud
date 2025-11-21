# FastAPI CRUD Application with Plain JavaScript
A complete, production-ready CRUD application built with FastAPI, SQLAlchemy, SQLite, and vanilla JavaScript.

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
    
    touch main.py database.py models.py schemas.py crud.py
    mkdir static
    touch static/index.html static/style.css static/app.js

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

        <!DOCTYPE html>
        <html lang="en">
        
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Simple CRUD App</title>
            <!-- Link external CSS -->
            <link rel="stylesheet" type="text/css" href="static/style.css">
        </head>
        
        <body>
            <div class="container">
                <h1>Simple CRUD Application</h1>
        
                <div id="message"></div>
        
                <!-- Create/Edit Form -->
                <div id="itemForm">
                    <h2 id="formTitle">Create New Item</h2>
                    <input type="hidden" id="itemId" value="">
        
                    <div class="form-group">
                        <label for="name">Name:</label>
                        <input type="text" id="name" required>
                    </div>
        
                    <div class="form-group">
                        <label for="description">Description:</label>
                        <textarea id="description"></textarea>
                    </div>
        
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="completed">
                            Completed
                        </label>
                    </div>
        
                    <div class="form-group">
                        <button onclick="saveItem()">Save</button>
                        <button onclick="resetForm()" class="cancel hidden" id="cancelBtn">Cancel</button>
                    </div>
                </div>
        
                <!-- Item List -->
                <div class="item-list">
                    <h2>Items</h2>
                    <div id="loading" class="loading">Loading items...</div>
                    <div id="itemsList"></div>
                </div>
            </div>
        
            <script src="/static/app.js"></script>
        </body>
        
        </html>

### style.css

            body {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f5f5f5;
    }
    
    .container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    h1 {
        color: #333;
        text-align: center;
    }
    
    .form-group {
        margin-bottom: 15px;
    }
    
    label {
        display: block;
        margin-bottom: 5px;
        color: #555;
        font-weight: bold;
    }
    
    input[type="text"],
    textarea {
        width: 100%;
        padding: 8px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
    }
    
    textarea {
        resize: vertical;
        min-height: 80px;
    }
    
    button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        margin-right: 10px;
    }
    
    button:hover {
        background-color: #45a049;
    }
    
    button.delete {
        background-color: #f44336;
    }
    
    button.delete:hover {
        background-color: #da190b;
    }
    
    button.cancel {
        background-color: #ff9800;
    }
    
    .item-list {
        margin-top: 30px;
    }
    
    .item-card {
        border: 1px solid #ddd;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 4px;
        background-color: #fafafa;
    }
    
    .item-card h3 {
        margin-top: 0;
        color: #333;
    }
    
    .item-actions {
        margin-top: 10px;
    }
    
    .loading {
        text-align: center;
        color: #666;
    }
    
    .error {
        color: #f44336;
        padding: 10px;
        background-color: #ffebee;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    
    .success {
        color: #4CAF50;
        padding: 10px;
        background-color: #e8f5e9;
        border-radius: 4px;
        margin-bottom: 10px;
    }
    
    .hidden {
        display: none;
    }

### app.js

                // Configuration
        const API_BASE_URL = '/api/items';
        
        // DOM elements
        const itemsList = document.getElementById('itemsList');
        const loading = document.getElementById('loading');
        const message = document.getElementById('message');
        const formTitle = document.getElementById('formTitle');
        const cancelBtn = document.getElementById('cancelBtn');
        const itemIdInput = document.getElementById('itemId');
        
        // Show message
        function showMessage(msg, isError = false) {
            message.textContent = msg;
            message.className = isError ? 'error' : 'success';
            setTimeout(() => {
                message.textContent = '';
                message.className = '';
            }, 3000);
        }
        
        // Fetch all items
        async function fetchItems() {
            loading.style.display = 'block';
            itemsList.innerHTML = '';
        
            try {
                const response = await fetch(API_BASE_URL);
                if (!response.ok) throw new Error('Failed to fetch items');
        
                const items = await response.json();
        
                loading.style.display = 'none';
        
                if (items.length === 0) {
                    itemsList.innerHTML = '<p>No items found. Create your first item!</p>';
                    return;
                }
        
                items.forEach(item => {
                    const itemCard = createItemCard(item);
                    itemsList.appendChild(itemCard);
                });
            } catch (error) {
                loading.style.display = 'none';
                showMessage('Error loading items: ' + error.message, true);
            }
        }
        
        // Create item card element
        function createItemCard(item) {
            const card = document.createElement('div');
            card.className = 'item-card';
        
            const title = document.createElement('h3');
            title.textContent = item.name;
        
            const description = document.createElement('p');
            description.textContent = item.description || 'No description';
        
            const status = document.createElement('p');
            status.innerHTML = `<strong>Status:</strong> ${item.completed ? 'Completed ✓' : 'Pending'}`;
        
            const actions = document.createElement('div');
            actions.className = 'item-actions';
        
            const editBtn = document.createElement('button');
            editBtn.textContent = 'Edit';
            editBtn.onclick = () => editItem(item);
        
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.className = 'delete';
            deleteBtn.onclick = () => deleteItem(item.id);
        
            actions.appendChild(editBtn);
            actions.appendChild(deleteBtn);
        
            card.appendChild(title);
            card.appendChild(description);
            card.appendChild(status);
            card.appendChild(actions);
        
            return card;
        }
        
        // Save item (create or update)
        async function saveItem() {
            const id = itemIdInput.value;
            const name = document.getElementById('name').value.trim();
            const description = document.getElementById('description').value.trim();
            const completed = document.getElementById('completed').checked;
        
            if (!name) {
                showMessage('Name is required', true);
                return;
            }
        
            const itemData = { name, description, completed };
        
            try {
                let response;
                if (id) {
                    // Update existing item
                    response = await fetch(`${API_BASE_URL}/${id}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(itemData),
                    });
                } else {
                    // Create new item
                    response = await fetch(API_BASE_URL, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(itemData),
                    });
                }
        
                if (!response.ok) throw new Error('Failed to save item');
        
                resetForm();
                fetchItems();
                showMessage(id ? 'Item updated successfully!' : 'Item created successfully!');
            } catch (error) {
                showMessage('Error saving item: ' + error.message, true);
            }
        }
        
        // Edit item
        function editItem(item) {
            document.getElementById('itemId').value = item.id;
            document.getElementById('name').value = item.name;
            document.getElementById('description').value = item.description || '';
            document.getElementById('completed').checked = item.completed;
        
            formTitle.textContent = 'Edit Item';
            cancelBtn.classList.remove('hidden');
        }
        
        // Reset form
        function resetForm() {
            document.getElementById('itemId').value = '';
            document.getElementById('name').value = '';
            document.getElementById('description').value = '';
            document.getElementById('completed').checked = false;
        
            formTitle.textContent = 'Create New Item';
            cancelBtn.classList.add('hidden');
        }
        
        // Delete item
        async function deleteItem(id) {
            if (!confirm('Are you sure you want to delete this item?')) return;
        
            try {
                const response = await fetch(`${API_BASE_URL}/${id}`, {
                    method: 'DELETE',
                });
        
                if (!response.ok) throw new Error('Failed to delete item');
        
                fetchItems();
                showMessage('Item deleted successfully!');
            } catch (error) {
                showMessage('Error deleting item: ' + error.message, true);
            }
        }
        
        // Initialize
        document.addEventListener('DOMContentLoaded', fetchItems);

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
