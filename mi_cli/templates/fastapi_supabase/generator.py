import os
import shutil
from .config_builder import crear_config_files
from .db_builder import crear_db_files


def generar_plantilla_fastapi_supabase(
    target_path: str, nombre: str, autor: str
):
    """Orquesta la creación de la plantilla FastAPI + Supabase."""
    app_dir = os.path.join(target_path, "app")
    routers_dir = os.path.join(app_dir, "routers")
    os.makedirs(routers_dir, exist_ok=True)

    # Copiar estáticos (Dockerfile, etc.) si existen
    files_dir = os.path.join(os.path.dirname(__file__), "files")
    if os.path.exists(files_dir):
        for file_name in os.listdir(files_dir):
            src_file = os.path.join(files_dir, file_name)
            dst_file = os.path.join(target_path, file_name)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dst_file)

    crear_config_files(app_dir, target_path, nombre)
    crear_db_files(app_dir, routers_dir)
    _crear_main(app_dir, nombre, autor)
    _crear_run_script(target_path)
    _crear_requirements(target_path, autor)


def _crear_main(app_dir: str, nombre: str, autor: str):
    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(
            f"# Creado por {autor}\n"
            "from contextlib import asynccontextmanager\n"
            "from fastapi import FastAPI\n"
            "from fastapi.middleware.cors import CORSMiddleware\n"
            "from app.config import CORS_ORIGINS\n"
            "from app.database import init_db\n"
            "from app.routers import items\n\n"
            "@asynccontextmanager\n"
            "async def lifespan(app: FastAPI):\n"
            "    init_db()\n"
            "    yield\n\n"
            f'app = FastAPI(title="{nombre}", lifespan=lifespan)\n\n'
            "app.add_middleware(\n"
            "    CORSMiddleware,\n"
            "    allow_origins=CORS_ORIGINS,\n"
            "    allow_credentials=True,\n"
            "    allow_methods=[\"*\"],\n"
            "    allow_headers=[\"*\"],\n"
            ")\n\n"
            "app.include_router(items.router)\n\n"
            '@app.get("/")\n'
            "def root():\n"
            '    return {"message": "API REST Supabase Serverless activa"}\n'
        )


def _crear_run_script(target_path: str):
    with open(os.path.join(target_path, "run.py"), "w", encoding="utf-8") as f:
        f.write(
            "import uvicorn\n\n"
            'if __name__ == "__main__":\n'
            '    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)\n'
        )


def _crear_requirements(target_path: str, autor: str):
    requirements_content = f"""# Dependencias para API REST en FastAPI + Supabase
# Generado por MoldPy - Autor: {autor}

fastapi
uvicorn[standard]
supabase
pydantic
python-dotenv
"""
    with open(
        os.path.join(target_path, "requirements.txt"), "w", encoding="utf-8"
    ) as f:
        f.write(requirements_content)