from pathlib import Path
from textwrap import dedent

def crear_config_files_supabase(app_dir: str, target_path: str, nombre: str):
    """Genera app/config.py, .env.example y README.md para FastAPI + Supabase."""
    app_path = Path(app_dir)
    target_p = Path(target_path)

    # 1. app/config.py
    config_content = dedent('''\
        import os
        from dotenv import load_dotenv

        load_dotenv()

        # Configuración CORS
        CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000")
        CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_RAW.split(",") if origin.strip()]

        # Credenciales Supabase
        SUPABASE_URL = os.getenv("SUPABASE_URL", "")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    ''')
    (app_path / "config.py").write_text(config_content, encoding="utf-8")

    # 2. .env.example
    env_content = dedent('''\
        # Configuración CORS
        CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000

        # Credenciales Supabase (Obtenlas en tu Dashboard de Supabase -> Project Settings -> API)
        SUPABASE_URL=https://tu-proyecto.supabase.co
        SUPABASE_KEY=tu-anon-key-o-service-role-key
    ''')
    (target_p / ".env.example").write_text(env_content, encoding="utf-8")

    # 3. README.md
    readme_content = dedent(f'''\
        # {nombre}

        API REST construida con FastAPI y Supabase.

        ## Configuración de Autenticación
        1. Copia `.env.example` a `.env`: `cp .env.example .env`
        2. Ingresa a tu panel de Supabase y copia la **Project URL** y la **anon API Key**.
        3. Pega los valores en el archivo `.env`.

        ## Ejecución Local
        1. Instala dependencias: `pip install -r requirements.txt`
        2. Inicia la API: `python run.py`
        3. Documentación interactiva en: `http://127.0.0.1:8000/docs`
    ''')
    (target_p / "README.md").write_text(readme_content, encoding="utf-8")