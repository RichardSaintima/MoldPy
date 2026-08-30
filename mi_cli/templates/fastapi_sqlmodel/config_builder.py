import os

def crear_config_files(app_dir: str, target_path: str, nombre: str):
    """Genera app/config.py, .env.example y README.md con soporte para CORS, Alembic y múltiples BD."""
    
    with open(os.path.join(app_dir, "config.py"), "w", encoding="utf-8") as f:
        f.write(
            'import os\n'
            'from dotenv import load_dotenv\n\n'
            'load_dotenv()\n\n'
            '# Configuración de CORS\n'
            'CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000")\n'
            'CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_RAW.split(",") if origin.strip()]\n\n'
            '# PRIORIDAD 1: DATABASE_URL explícita (Si el usuario la pone, SIEMPRE manda)\n'
            'RAW_DATABASE_URL = os.getenv("DATABASE_URL")\n\n'
            'if RAW_DATABASE_URL:\n'
            '    DATABASE_URL = RAW_DATABASE_URL\n'
            'else:\n'
            '    # PRIORIDAD 2: Armar URL desde credenciales individuales si no existe DATABASE_URL\n'
            '    DB_DRIVER = os.getenv("DB_DRIVER", "").lower()\n'
            '    DB_USER = os.getenv("DB_USER")\n'
            '    DB_PASSWORD = os.getenv("DB_PASSWORD")\n'
            '    DB_HOST = os.getenv("DB_HOST", "localhost")\n'
            '    DB_NAME = os.getenv("DB_NAME")\n\n'
            '    if DB_USER and DB_PASSWORD and DB_NAME:\n'
            '        if DB_DRIVER in ["mysql", "mariadb"]:\n'
            '            DB_PORT = os.getenv("DB_PORT", "3306")\n'
            '            DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"\n'
            '        else:\n'
            '            # Postgres / PostgreSQL por defecto\n'
            '            DB_PORT = os.getenv("DB_PORT", "5432")\n'
            '            DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"\n'
            '    else:\n'
            '        # PRIORIDAD 3: Respaldo a SQLite solo si NO hay nada configurado en el .env\n'
            '        DATABASE_URL = "sqlite:///./database.db"\n'
        )

    with open(os.path.join(target_path, ".env.example"), "w", encoding="utf-8") as f:
        f.write(
            '# Configuración CORS (orígenes permitidos separados por comas)\n'
            'CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000\n\n'
            '# OPCIÓN A: Credenciales individuales (Ideal para desarrollo local)\n'
            'DB_DRIVER=postgresql  # Opciones: postgresql / mysql\n'
            'DB_USER=postgres\n'
            'DB_PASSWORD=admin\n'
            'DB_HOST=localhost\n'
            'DB_PORT=5432          # 5432 para Postgres, 3306 para MySQL\n'
            'DB_NAME=prueba_api\n\n'
            '# OPCIÓN B: URL directa (Descomentar para usar Supabase, Docker, producción o SQLite)\n'
            '# DATABASE_URL=postgresql+psycopg2://postgres:admin@localhost:5432/prueba_api\n'
            '# DATABASE_URL=sqlite:///./database.db\n'
        )

    with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f'# {nombre}\n\n'
            'API REST construida con FastAPI, SQLModel, Alembic y Docker.\n\n'
            '## Ejecución Local\n'
            '1. Copia `.env.example` a `.env`: `cp .env.example .env`\n'
            '2. Instala dependencias: `pip install -r requirements.txt`\n'
            '3. Inicia el servidor: `python run.py`\n'
            '4. Accede a la documentación interactiva: `http://127.0.0.1:8000/docs`\n\n'
            '## Migraciones de Base de Datos (Alembic)\n'
            'Si realizas cambios en los modelos de `app/models/`:\n\n'
            '1. Genera una nueva migración automática:\n'
            '```bash\n'
            'alembic revision --autogenerate -m "descripcion_del_cambio"\n'
            '```\n\n'
            '2. Aplica los cambios a la base de datos:\n'
            '```bash\n'
            'alembic upgrade head\n'
            '```\n\n'
            '## Ejecución con Docker\n'
            '```bash\n'
            'docker compose up --build\n'
            '```\n'
        )