from pathlib import Path
from textwrap import dedent

def crear_db_files_supabase(app_dir: str, routers_dir: str):
    """Genera la capa de datos Supabase con cliente seguro e inyección de dependencias."""
    app_path = Path(app_dir)
    routers_path = Path(routers_dir)
    models_path = app_path / "models"
    models_path.mkdir(parents=True, exist_ok=True)

    # 1. app/database.py
    db_content = dedent('''\
        import logging
        from supabase import create_client, Client
        from fastapi import HTTPException, status
        from app.config import SUPABASE_URL, SUPABASE_KEY

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        db: Client = None

        def init_db():
            global db
            if not SUPABASE_URL or not SUPABASE_KEY:
                logger.warning("Variables SUPABASE_URL o SUPABASE_KEY no configuradas en el entorno.")
                db = None
                return

            try:
                db = create_client(SUPABASE_URL, SUPABASE_KEY)
                logger.info("Conexión con Supabase inicializada correctamente.")
            except Exception as e:
                logger.error(f"Fallo al conectar con Supabase: {e}")
                db = None

        def get_db() -> Client:
            """Valida que la conexión a Supabase esté activa antes de procesar una petición HTTP."""
            if db is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="El servicio de Supabase no está configurado. Revisa las variables en el archivo .env"
                )
            return db
    ''')
    (app_path / "database.py").write_text(db_content, encoding="utf-8")

    # 2. app/models/item.py
    item_model_content = dedent('''\
        from typing import Optional
        from pydantic import BaseModel, Field

        class ItemBase(BaseModel):
            title: str = Field(..., min_length=1, max_length=100)
            description: Optional[str] = None
            price: float = Field(..., gt=0)

        class ItemCreate(ItemBase):
            pass

        class ItemUpdate(BaseModel):
            title: Optional[str] = Field(None, min_length=1, max_length=100)
            description: Optional[str] = None
            price: Optional[float] = Field(None, gt=0)

        class ItemResponse(ItemBase):
            id: int | str
            created_at: Optional[str] = None
            updated_at: Optional[str] = None
    ''')
    (models_path / "item.py").write_text(item_model_content, encoding="utf-8")

    # app/models/__init__.py
    models_init_content = dedent('''\
        import importlib
        import pkgutil

        for _, module_name, _ in pkgutil.iter_modules(__path__):
            if not module_name.startswith("_"):
                importlib.import_module(f"{__name__}.{module_name}")
    ''')
    (models_path / "__init__.py").write_text(models_init_content, encoding="utf-8")

    # 3. app/routers/items.py (Operaciones CRUD nativas de Supabase)
    router_content = dedent('''\
        from typing import List
        from datetime import datetime, timezone
        from fastapi import APIRouter, HTTPException, Query, status, Depends
        from supabase import Client
        from app.database import get_db
        from app.models.item import ItemCreate, ItemUpdate, ItemResponse

        router = APIRouter(prefix="/items", tags=["Items"])
        TABLE_NAME = "items"

        @router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
        def create_item(item: ItemCreate, db: Client = Depends(get_db)):
            now = datetime.now(timezone.utc).isoformat()
            data = item.model_dump()
            data["created_at"] = now
            data["updated_at"] = now
            
            res = db.table(TABLE_NAME).insert(data).execute()
            if not res.data:
                raise HTTPException(status_code=400, detail="Error al crear el elemento en Supabase")
            return res.data[0]

        @router.get("/", response_model=List[ItemResponse])
        def read_items(
            limit: int = Query(default=20, le=100, ge=1),
            offset: int = Query(default=0, ge=0),
            db: Client = Depends(get_db)
        ):
            # Paginación usando range() en Supabase
            res = db.table(TABLE_NAME).select("*").range(offset, offset + limit - 1).execute()
            return res.data

        @router.get("/{item_id}", response_model=ItemResponse)
        def read_item(item_id: str, db: Client = Depends(get_db)):
            res = db.table(TABLE_NAME).select("*").eq("id", item_id).execute()
            if not res.data:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            return res.data[0]

        @router.patch("/{item_id}", response_model=ItemResponse)
        def update_item(item_id: str, item_update: ItemUpdate, db: Client = Depends(get_db)):
            update_data = {k: v for k, v in item_update.model_dump().items() if v is not None}
            if update_data:
                update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
                res = db.table(TABLE_NAME).update(update_data).eq("id", item_id).execute()
                if not res.data:
                    raise HTTPException(status_code=404, detail="Item no encontrado")
                return res.data[0]
            
            # Si no hay datos que actualizar, retornamos el estado actual
            return read_item(item_id, db)

        @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_item(item_id: str, db: Client = Depends(get_db)):
            res = db.table(TABLE_NAME).delete().eq("id", item_id).execute()
            if not res.data:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            return None
    ''')
    (routers_path / "items.py").write_text(router_content, encoding="utf-8")