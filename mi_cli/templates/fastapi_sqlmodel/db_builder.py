import os

def crear_db_files(app_dir: str, routers_dir: str):
    """Genera la capa de base de datos con modelos modulares y carga dinámica automática."""
    
    with open(os.path.join(app_dir, "database.py"), "w", encoding="utf-8") as f:
        f.write(
            'from sqlmodel import SQLModel, create_engine, Session\n'
            'from app.config import DATABASE_URL\n\n'
            'connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}\n'
            'engine = create_engine(DATABASE_URL, connect_args=connect_args)\n\n'
            'def get_session():\n'
            '    with Session(engine) as session:\n'
            '        yield session\n\n'
            'def init_db():\n'
            '    import app.models  # Carga todos los modelos automáticamente\n'
            '    SQLModel.metadata.create_all(engine)\n'
        )

    models_dir = os.path.join(app_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    with open(os.path.join(models_dir, "item.py"), "w", encoding="utf-8") as f:
        f.write(
            'from typing import Optional\n'
            'from sqlmodel import SQLModel, Field\n\n'
            'class ItemBase(SQLModel):\n'
            '    title: str = Field(index=True)\n'
            '    description: Optional[str] = None\n'
            '    price: float\n\n'
            'class Item(ItemBase, table=True):\n'
            '    id: Optional[int] = Field(default=None, primary_key=True)\n\n'
            'class ItemCreate(ItemBase):\n'
            '    pass\n\n'
            'class ItemRead(ItemBase):\n'
            '    id: int\n\n'
            'class ItemUpdate(SQLModel):\n'
            '    title: Optional[str] = None\n'
            '    description: Optional[str] = None\n'
            '    price: Optional[float] = None\n'
        )

    with open(os.path.join(models_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write(
            'import importlib\n'
            'import pkgutil\n\n'
            '# Carga automáticamente todos los archivos .py de la carpeta models/\n'
            'for _, module_name, _ in pkgutil.iter_modules(__path__):\n'
            '    if not module_name.startswith("_"):\n'
            '        importlib.import_module(f"{__name__}.{module_name}")\n'
        )

    with open(os.path.join(routers_dir, "items.py"), "w", encoding="utf-8") as f:
        f.write(
            'from typing import List\n'
            'from fastapi import APIRouter, Depends, HTTPException, status\n'
            'from sqlmodel import Session, select\n'
            'from app.database import get_session\n'
            'from app.models.item import Item, ItemCreate, ItemRead, ItemUpdate\n\n'
            'router = APIRouter(prefix="/items", tags=["Items"])\n\n'
            '@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)\n'
            'def create_item(item: ItemCreate, session: Session = Depends(get_session)):\n'
            '    db_item = Item.model_validate(item)\n'
            '    session.add(db_item)\n'
            '    session.commit()\n'
            '    session.refresh(db_item)\n'
            '    return db_item\n\n'
            '@router.get("/", response_model=List[ItemRead])\n'
            'def read_items(offset: int = 0, limit: int = 100, session: Session = Depends(get_session)):\n'
            '    items = session.exec(select(Item).offset(offset).limit(limit)).all()\n'
            '    return items\n\n'
            '@router.get("/{item_id}", response_model=ItemRead)\n'
            'def read_item(item_id: int, session: Session = Depends(get_session)):\n'
            '    item = session.get(Item, item_id)\n'
            '    if not item:\n'
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            '    return item\n\n'
            '@router.patch("/{item_id}", response_model=ItemRead)\n'
            'def update_item(item_id: int, item_update: ItemUpdate, session: Session = Depends(get_session)):\n'
            '    db_item = session.get(Item, item_id)\n'
            '    if not db_item:\n'
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            '    item_data = item_update.model_dump(exclude_unset=True)\n'
            '    for key, value in item_data.items():\n'
            '        setattr(db_item, key, value)\n'
            '    session.add(db_item)\n'
            '    session.commit()\n'
            '    session.refresh(db_item)\n'
            '    return db_item\n\n'
            '@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)\n'
            'def delete_item(item_id: int, session: Session = Depends(get_session)):\n'
            '    item = session.get(Item, item_id)\n'
            '    if not item:\n'
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            '    session.delete(item)\n'
            '    session.commit()\n'
            '    return None\n'
        )