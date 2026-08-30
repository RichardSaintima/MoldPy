import os
import shutil
from .config_builder import crear_config_files
from .db_builder import crear_db_files
from .alembic_builder import crear_alembic_files

def generar_plantilla_fastapi_sqlmodel(target_path: str, nombre: str, autor: str):
    """Orquesta la creación de la plantilla copiando plantillas y llamando constructores."""
    app_dir = os.path.join(target_path, "app")
    routers_dir = os.path.join(app_dir, "routers")
    os.makedirs(routers_dir, exist_ok=True)

    # 1. Copiar archivos estáticos de la carpeta files/ (Dockerfile y docker-compose.yml)
    files_dir = os.path.join(os.path.dirname(__file__), "files")
    if os.path.exists(files_dir):
        for file_name in os.listdir(files_dir):
            src_file = os.path.join(files_dir, file_name)
            dst_file = os.path.join(target_path, file_name)
            if os.path.isfile(src_file):
                shutil.copy(src_file, dst_file)

    # 2. Generar archivos lógicos y de configuración
    crear_config_files(app_dir, target_path, nombre)
    crear_db_files(app_dir, routers_dir)
    crear_alembic_files(target_path)
    _crear_main(app_dir, nombre, autor)
    _crear_run_script(target_path)
    _crear_requirements(target_path, autor)


def _crear_main(app_dir: str, nombre: str, autor: str):
    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'from fastapi import FastAPI\n'
            'from fastapi.middleware.cors import CORSMiddleware\n'
            'from app.config import CORS_ORIGINS\n'
            'from app.routers import items\n\n'
            f'app = FastAPI(title="{nombre}")\n\n'
            '# Configuración Middleware CORS\n'
            'app.add_middleware(\n'
            '    CORSMiddleware,\n'
            '    allow_origins=CORS_ORIGINS,\n'
            '    allow_credentials=True,\n'
            '    allow_methods=["*"],\n'
            '    allow_headers=["*"],\n'
            ')\n\n'
            'app.include_router(items.router)\n\n'
            '@app.get("/")\n'
            'def root():\n'
            '    return {"message": "API con SQLModel y Docker activa"}\n'
        )


def _crear_run_script(target_path: str):
    with open(os.path.join(target_path, "run.py"), "w", encoding="utf-8") as f:
        f.write(
            'import uvicorn\n\n'
            'if __name__ == "__main__":\n'
            '    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)\n'
        )


def _crear_requirements(target_path: str, autor: str):
    requirements_content = f"""# Dependencias para API REST en FastAPI + SQLModel (SQL)
# Generado por MoldPy - Autor: {autor}

fastapi
uvicorn[standard]
sqlmodel
alembic
python-dotenv
psycopg2-binary
pymysql
"""
    with open(os.path.join(target_path, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(requirements_content)