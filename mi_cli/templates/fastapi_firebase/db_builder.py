import os


def crear_db_files(app_dir: str, routers_dir: str):
    """Genera la capa de datos NoSQL Serverless con Firebase Admin SDK mejorado."""

    # 1. Generación de app/database.py con soporte para JSON y Variables de Entorno
    with open(os.path.join(app_dir, "database.py"), "w", encoding="utf-8") as f:
        f.write(
            "import os\n"
            "import json\n"
            "import firebase_admin\n"
            "from firebase_admin import credentials, firestore\n"
            "from app.config import FIREBASE_CREDENTIALS_PATH\n\n"
            "db = None\n\n"
            "def init_db():\n"
            "    global db\n"
            "    if not firebase_admin._apps:\n"
            "        # 1. Cargar archivo JSON local si existe (Desarrollo local)\n"
            "        if os.path.exists(FIREBASE_CREDENTIALS_PATH):\n"
            "            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)\n"
            "            firebase_admin.initialize_app(cred)\n"
            "        # 2. Cargar desde Variables de Entorno (Producción / Nube)\n"
            '        elif os.getenv("FIREBASE_PRIVATE_KEY"):\n'
            '            private_key = os.getenv("FIREBASE_PRIVATE_KEY").replace("\\\\n", "\\n")\n'
            "            cred_dict = {\n"
            '                "type": "service_account",\n'
            '                "project_id": os.getenv("FIREBASE_PROJECT_ID"),\n'
            '                "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),\n'
            '                "private_key": private_key,\n'
            '                "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),\n'
            '                "client_id": os.getenv("FIREBASE_CLIENT_ID"),\n'
            '                "auth_uri": "https://accounts.google.com/o/oauth2/auth",\n'
            '                "token_uri": "https://oauth2.googleapis.com/token",\n'
            "            }\n"
            "            cred = credentials.Certificate(cred_dict)\n"
            "            firebase_admin.initialize_app(cred)\n"
            "        # 3. Fallback: GCP ADC o Emuladores\n"
            "        else:\n"
            "            firebase_admin.initialize_app()\n\n"
            "    db = firestore.client()\n"
        )

    # 2. Crear app/models/
    models_dir = os.path.join(app_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    # app/models/item.py con marcas de tiempo (timestamps)
    with open(os.path.join(models_dir, "item.py"), "w", encoding="utf-8") as f:
        f.write(
            "from typing import Optional\n"
            "from pydantic import BaseModel, Field\n"
            "from datetime import datetime\n\n"
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
            "    id: str\n"
            "    created_at: Optional[str] = None\n"
            "    updated_at: Optional[str] = None\n"
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

    # 3. app/routers/items.py con Paginación y Marcas de Tiempo
    with open(os.path.join(routers_dir, "items.py"), "w", encoding="utf-8") as f:
        f.write(
            "from typing import List, Optional\n"
            "from datetime import datetime, timezone\n"
            "from fastapi import APIRouter, HTTPException, Query, status\n"
            "from google.cloud.firestore_v1 import Query as FirestoreQuery\n"
            "from app.database import db\n"
            "from app.models.item import ItemCreate, ItemUpdate, ItemResponse\n\n"
            'router = APIRouter(prefix="/items", tags=["Items"])\n'
            'COLLECTION_NAME = "items"\n\n'
            '@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)\n'
            "def create_item(item: ItemCreate):\n"
            "    doc_ref = db.collection(COLLECTION_NAME).document()\n"
            "    now = datetime.now(timezone.utc).isoformat()\n"
            "    data = item.model_dump()\n"
            '    data["created_at"] = now\n'
            '    data["updated_at"] = now\n'
            "    doc_ref.set(data)\n"
            '    data["id"] = doc_ref.id\n'
            "    return data\n\n"
            '@router.get("/", response_model=List[ItemResponse])\n'
            "def read_items(\n"
            "    limit: int = Query(default=20, le=100, ge=1),\n"
            "    offset: int = Query(default=0, ge=0)\n"
            "):\n"
            "    # Consulta optimizada con paginación en Firestore\n"
            "    query = db.collection(COLLECTION_NAME).limit(limit).offset(offset)\n"
            "    docs = query.stream()\n"
            "    items = []\n"
            "    for doc in docs:\n"
            "        data = doc.to_dict()\n"
            '        data["id"] = doc.id\n'
            "        items.append(data)\n"
            "    return items\n\n"
            '@router.get("/{item_id}", response_model=ItemResponse)\n'
            "def read_item(item_id: str):\n"
            "    doc = db.collection(COLLECTION_NAME).document(item_id).get()\n"
            "    if not doc.exists:\n"
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            "    data = doc.to_dict()\n"
            '    data["id"] = doc.id\n'
            "    return data\n\n"
            '@router.patch("/{item_id}", response_model=ItemResponse)\n'
            "def update_item(item_id: str, item_update: ItemUpdate):\n"
            "    doc_ref = db.collection(COLLECTION_NAME).document(item_id)\n"
            "    if not doc_ref.get().exists:\n"
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            "    update_data = {k: v for k, v in item_update.model_dump().items() if v is not None}\n"
            "    if update_data:\n"
            '        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()\n'
            "        doc_ref.update(update_data)\n"
            "    updated_doc = doc_ref.get().to_dict()\n"
            '    updated_doc["id"] = doc_ref.id\n'
            "    return updated_doc\n\n"
            '@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)\n'
            "def delete_item(item_id: str):\n"
            "    doc_ref = db.collection(COLLECTION_NAME).document(item_id)\n"
            "    if not doc_ref.get().exists:\n"
            '        raise HTTPException(status_code=404, detail="Item no encontrado")\n'
            "    doc_ref.delete()\n"
            "    return None\n"
        )