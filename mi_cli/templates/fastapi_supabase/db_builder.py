import os


def crear_db_files(app_dir: str, routers_dir: str):
    """Genera la capa de datos Serverless utilizando el SDK oficial de Supabase."""

    # 1. app/database.py
    with open(os.path.join(app_dir, "database.py"), "w", encoding="utf-8") as f:
        f.write(
            "from supabase import create_client, Client\n"
            "from app.config import SUPABASE_URL, SUPABASE_KEY\n\n"
            "supabase: Client = None\n\n"
            "def init_db():\n"
            "    global supabase\n"
            "    if not SUPABASE_URL or not SUPABASE_KEY:\n"
            '        raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configuradas en el archivo .env")\n'
            "    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)\n"
        )

    # 2. app/models/
    models_dir = os.path.join(app_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    # app/models/item.py (Modelos Pydantic)
    with open(os.path.join(models_dir, "item.py"), "w", encoding="utf-8") as f:
        f.write(
            "from typing import Optional\n"
            "from pydantic import BaseModel, Field\n\n"
            "class ItemBase(BaseModel):\n"
            "    title: str = Field(..., min_length=1, max_length=100)\n"
            "    description: Optional[str] = None\n"
            "    price: float = Field(..., gt=0)\n\n"
            "class ItemCreate(ItemBase):\n"
            "    pass\n\n"
            "class ItemUpdate(BaseModel):\n"
            "    title: Optional[str] = Field(None, min_length=1, max_length=100)\n"
            "    description: Optional[str] = None\n"
            "    price: Optional[float] = Field(None, gt=0)\n\n"
            "class ItemResponse(ItemBase):\n"
            "    id: int\n"
            "    created_at: Optional[str] = None\n"
        )

    # app/models/__init__.py
    with open(
        os.path.join(models_dir, "__init__.py"), "w", encoding="utf-8"
    ) as f:
        f.write(
            "import importlib\n"
            "import pkgutil\n\n"
            "for _, module_name, _ in pkgutil.iter_modules(__path__):\n"
            '    if not module_name.startswith("_"):\n'
            '        importlib.import_module(f"{__name__}.{module_name}")\n'
        )

    # 3. app/routers/items.py (CRUD con SDK de Supabase)
    with open(os.path.join(routers_dir, "items.py"), "w", encoding="utf-8") as f:
        f.write(
            "from typing import List\n"
            "from fastapi import APIRouter, HTTPException, Query, status\n"
            "from app.database import supabase\n"
            "from app.models.item import ItemCreate, ItemUpdate, ItemResponse\n\n"
            'router = APIRouter(prefix="/items", tags=["Items"])\n'
            'TABLE_NAME = "items"\n\n'
            '@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)\n'
            "def create_item(item: ItemCreate):\n"
            "    response = supabase.table(TABLE_NAME).insert(item.model_dump()).execute()\n"
            "    if not response.data:\n"
            '        raise HTTPException(status_code=400, detail="Error al crear el registro en Supabase")\n'
            "    return response.data[0]\n\n"
            '@router.get("/", response_model=List[ItemResponse])\n'
            "def read_items(\n"
            "    limit: int = Query(default=20, le=100, ge=1),\n"
            "    offset: int = Query(default=0, ge=0)\n"
            "):\n"
            "    response = supabase.table(TABLE_NAME).select(\"*\").range(offset, offset + limit - 1).execute()\n"
            "    return response.data\n\n"
            '@router.get("/{item_id}", response_model=ItemResponse)\n'
            "def read_item(item_id: int):\n"
            "    response = supabase.table(TABLE_NAME).select(\"*\").eq(\"id\", item_id).execute()\n"
            "    if not response.data:\n"
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            "    return response.data[0]\n\n"
            '@router.patch("/{item_id}", response_model=ItemResponse)\n'
            "def update_item(item_id: int, item_update: ItemUpdate):\n"
            "    update_data = {k: v for k, v in item_update.model_dump().items() if v is not None}\n"
            "    if not update_data:\n"
            '        raise HTTPException(status_code=400, detail="No hay campos para actualizar")\n'
            "    response = supabase.table(TABLE_NAME).update(update_data).eq(\"id\", item_id).execute()\n"
            "    if not response.data:\n"
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            "    return response.data[0]\n\n"
            '@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)\n'
            "def delete_item(item_id: int):\n"
            "    response = supabase.table(TABLE_NAME).delete().eq(\"id\", item_id).execute()\n"
            "    if not response.data:\n"
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            "    return None\n"
        )