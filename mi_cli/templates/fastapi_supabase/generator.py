import shutil
from pathlib import Path
from textwrap import dedent
from .config_builder import crear_config_files_supabase
from .db_builder import crear_db_files_supabase

def generar_plantilla_fastapi_supabase(target_path: str, nombre: str, autor: str):
    """Orquesta la creación de la plantilla FastAPI + Supabase."""
    target_p = Path(target_path)
    app_dir = target_p / "app"
    routers_dir = app_dir / "routers"
    routers_dir.mkdir(parents=True, exist_ok=True)

    # 1. Archivos estáticos
    files_dir = Path(__file__).parent / "files"
    if files_dir.exists():
        for file_path in files_dir.iterdir():
            if file_path.is_file():
                shutil.copy(file_path, target_p / file_path.name)

    # 2. Generar módulos
    crear_config_files_supabase(str(app_dir), str(target_p), nombre)
    crear_db_files_supabase(str(app_dir), str(routers_dir))
    _crear_main(str(app_dir), nombre, autor)
    _crear_run_script(str(target_p))
    _crear_requirements(str(target_p), autor)


def _crear_main(app_dir: str, nombre: str, autor: str):
    main_content = dedent(f'''\
        # Creado por {autor}
        from contextlib import asynccontextmanager
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from app.config import CORS_ORIGINS
        from app.database import init_db
        from app.routers import items

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            init_db()
            yield

        app = FastAPI(title="{nombre}", lifespan=lifespan)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(items.router)

        @app.get("/")
        def root():
            return {{"message": "API REST FastAPI + Supabase activa"}}
    ''')
    (Path(app_dir) / "main.py").write_text(main_content, encoding="utf-8")


def _crear_run_script(target_path: str):
    run_content = dedent('''\
        import uvicorn

        if __name__ == "__main__":
            uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    ''')
    (Path(target_path) / "run.py").write_text(run_content, encoding="utf-8")


def _crear_requirements(target_path: str, autor: str):
    req_content = dedent(f'''\
        # Dependencias para API REST FastAPI + Supabase
        # Generado por MoldPy - Autor: {autor}

        fastapi
        uvicorn[standard]
        supabase
        pydantic
        python-dotenv
    ''')
    (Path(target_path) / "requirements.txt").write_text(req_content, encoding="utf-8")