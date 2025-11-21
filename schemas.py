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
        from_attributes = True # For this model (Item), you can populate it from an object’s attributes (like a SQLAlchemy ORM instance), not just from a dict