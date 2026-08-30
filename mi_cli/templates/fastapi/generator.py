import os


def generar_plantilla_fastapi(target_path: str, nombre: str, autor: str):
    """Genera la estructura básica e independiente para un proyecto FastAPI listo para usar."""
    app_dir = os.path.join(target_path, "app")
    routers_dir = os.path.join(app_dir, "routers")
    os.makedirs(routers_dir, exist_ok=True)

    # 1. Configuración de entorno y CORS (app/config.py)
    with open(os.path.join(app_dir, "config.py"), "w", encoding="utf-8") as f:
        f.write(
            "import os\n"
            "from dotenv import load_dotenv\n\n"
            "load_dotenv()\n\n"
            "# Configuración CORS\n"
            'CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000")\n'
            'CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_RAW.split(",") if origin.strip()]\n'
        )

    # 2. Router de prueba (app/routers/items.py)
    with open(os.path.join(routers_dir, "items.py"), "w", encoding="utf-8") as f:
        f.write(
            "from typing import Optional\n"
            "from fastapi import APIRouter, status\n"
            "from pydantic import BaseModel, Field\n\n"
            'router = APIRouter(prefix="/items", tags=["Items"])\n\n'
            "class Item(BaseModel):\n"
            "    id: Optional[int] = None\n"
            "    name: str = Field(..., min_length=1)\n"
            "    price: float = Field(..., gt=0)\n\n"
            '@router.get("/", response_model=list[Item])\n'
            "def list_items():\n"
            '    return [{"id": 1, "name": "Ejemplo de producto", "price": 19.99}]\n\n'
            '@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)\n'
            "def create_item(item: Item):\n"
            '    return {"id": 1, **item.model_dump()}\n'
        )

    # 3. Módulo routers (app/routers/__init__.py)
    with open(os.path.join(routers_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Módulo de rutas de la aplicación\n")

    # 4. Archivo principal (app/main.py)
    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(
            f"# Creado por {autor}\n"
            "from fastapi import FastAPI\n"
            "from fastapi.middleware.cors import CORSMiddleware\n"
            "from app.config import CORS_ORIGINS\n"
            "from app.routers import items\n\n"
            f'app = FastAPI(title="{nombre}")\n\n'
            "app.add_middleware(\n"
            "    CORSMiddleware,\n"
            "    allow_origins=CORS_ORIGINS,\n"
            "    allow_credentials=True,\n"
            "    allow_methods=[\"*\"],\n"
            "    allow_headers=[\"*\"],\n"
            ")\n\n"
            "app.include_router(items.router)\n\n"
            '@app.get("/")\n'
            "def read_root():\n"
            '    return {"message": "¡API corriendo exitosamente!"}\n'
        )

    # 5. Archivo ejecutable (run.py)
    with open(os.path.join(target_path, "run.py"), "w", encoding="utf-8") as f:
        f.write(
            "import uvicorn\n\n"
            'if __name__ == "__main__":\n'
            '    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)\n'
        )

    # 6. Variables de entorno de ejemplo (.env.example)
    with open(os.path.join(target_path, ".env.example"), "w", encoding="utf-8") as f:
        f.write(
            "# Configuración CORS (Separados por coma)\n"
            "CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000\n"
        )

    # 7. Lista de dependencias (requirements.txt)
    with open(os.path.join(target_path, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(
            f"# Dependencias básicas para FastAPI\n"
            f"# Generado por MoldPy - Autor: {autor}\n\n"
            "fastapi\n"
            "uvicorn[standard]\n"
            "pydantic\n"
            "python-dotenv\n"
        )

    # 8. Documentación (README.md)
    with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f"# {nombre}\n\n"
            "API REST básica creada con FastAPI.\n\n"
            "## Ejecución Local\n"
            "1. Copia `.env.example` a `.env`: `cp .env.example .env`\n"
            "2. Instala dependencias: `pip install -r requirements.txt`\n"
            "3. Inicia el servidor de desarrollo: `python run.py`\n"
            "4. Revisa la documentación interactiva en: `http://127.0.0.1:8000/docs`\n"
        )