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