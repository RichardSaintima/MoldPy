from pathlib import Path
from textwrap import dedent

def crear_db_files(app_dir: str, routers_dir: str):
    """Genera la capa de datos NoSQL Serverless con Firebase Admin SDK mejorado y manejo defensivo de errores."""
    app_path = Path(app_dir)
    routers_path = Path(routers_dir)
    models_path = app_path / "models"
    models_path.mkdir(parents=True, exist_ok=True)

    # 1. app/database.py con inicialización segura e inyección de dependencia get_db
    db_content = dedent('''\
        import os
        import logging
        import firebase_admin
        from firebase_admin import credentials, firestore
        from fastapi import HTTPException, status
        from app.config import FIREBASE_CREDENTIALS_PATH

        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        db = None

        def init_db():
            global db
            if firebase_admin._apps:
                db = firestore.client()
                return

            try:
                # 1. Intentar cargar el archivo JSON local
                if os.path.exists(FIREBASE_CREDENTIALS_PATH):
                    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase inicializado mediante archivo de credenciales local.")
                
                # 2. Intentar cargar mediante Variables de Entorno de Producción
                elif os.getenv("FIREBASE_PRIVATE_KEY"):
                    private_key = os.getenv("FIREBASE_PRIVATE_KEY").replace("\\\\n", "\\n")
                    cred_dict = {
                        "type": "service_account",
                        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
                        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
                        "private_key": private_key,
                        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
                        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                    logger.info("Firebase inicializado mediante variables de entorno.")

                # 3. Intentar credenciales implícitas de Google Cloud Platform (ADC)
                else:
                    firebase_admin.initialize_app()
                    logger.info("Firebase inicializado mediante Google Application Default Credentials.")

                db = firestore.client()

            except Exception as e:
                logger.error(f"Fallo al inicializar Firebase Firestore: {e}")
                db = None

        def get_db():
            """Inyección de dependencia para asegurar que la conexión esté activa antes de procesar una petición."""
            if db is None:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="El servicio de base de datos no está disponible. Revisa las credenciales de Firebase en el archivo .env"
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
            id: str
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

    # 3. app/routers/items.py con uso de Depends(get_db)
    router_content = dedent('''\
        from typing import List
        from datetime import datetime, timezone
        from fastapi import APIRouter, HTTPException, Query, status, Depends
        from app.database import get_db
        from app.models.item import ItemCreate, ItemUpdate, ItemResponse

        router = APIRouter(prefix="/items", tags=["Items"])
        COLLECTION_NAME = "items"

        @router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
        def create_item(item: ItemCreate, db=Depends(get_db)):
            doc_ref = db.collection(COLLECTION_NAME).document()
            now = datetime.now(timezone.utc).isoformat()
            data = item.model_dump()
            data["created_at"] = now
            data["updated_at"] = now
            doc_ref.set(data)
            data["id"] = doc_ref.id
            return data

        @router.get("/", response_model=List[ItemResponse])
        def read_items(
            limit: int = Query(default=20, le=100, ge=1),
            offset: int = Query(default=0, ge=0),
            db=Depends(get_db)
        ):
            query = db.collection(COLLECTION_NAME).limit(limit).offset(offset)
            docs = query.stream()
            items = []
            for doc in docs:
                data = doc.to_dict()
                data["id"] = doc.id
                items.append(data)
            return items

        @router.get("/{item_id}", response_model=ItemResponse)
        def read_item(item_id: str, db=Depends(get_db)):
            doc = db.collection(COLLECTION_NAME).document(item_id).get()
            if not doc.exists:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            data = doc.to_dict()
            data["id"] = doc.id
            return data

        @router.patch("/{item_id}", response_model=ItemResponse)
        def update_item(item_id: str, item_update: ItemUpdate, db=Depends(get_db)):
            doc_ref = db.collection(COLLECTION_NAME).document(item_id)
            if not doc_ref.get().exists:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            
            update_data = {k: v for k, v in item_update.model_dump().items() if v is not None}
            if update_data:
                update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
                doc_ref.update(update_data)
            
            updated_doc = doc_ref.get().to_dict()
            updated_doc["id"] = doc_ref.id
            return updated_doc

        @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
        def delete_item(item_id: str, db=Depends(get_db)):
            doc_ref = db.collection(COLLECTION_NAME).document(item_id)
            if not doc_ref.get().exists:
                raise HTTPException(status_code=404, detail="Item no encontrado")
            doc_ref.delete()
            return None
    ''')
    (routers_path / "items.py").write_text(router_content, encoding="utf-8")