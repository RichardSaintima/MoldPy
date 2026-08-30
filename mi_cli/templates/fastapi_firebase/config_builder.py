from pathlib import Path
from textwrap import dedent

def crear_config_files(app_dir: str, target_path: str, nombre: str):
    """Genera app/config.py, .env.example y README.md para NoSQL Serverless (Firebase)."""
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

        # Ruta de credenciales Firebase/Firestore (Desarrollo local)
        FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
    ''')
    (app_path / "config.py").write_text(config_content, encoding="utf-8")

    # 2. .env.example
    env_content = dedent('''\
        # Configuración CORS
        CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000

        # OPCIÓN A: Archivo local (Desarrollo)
        FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json

        # OPCIÓN B: Variables de entorno individuales (Producción / Nube)
        # FIREBASE_PROJECT_ID=tu-proyecto-id
        # FIREBASE_PRIVATE_KEY_ID=clave-id
        # FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
        # FIREBASE_CLIENT_EMAIL=firebase-adminsdk@tu-proyecto.iam.gserviceaccount.com
        # FIREBASE_CLIENT_ID=123456789
    ''')
    (target_p / ".env.example").write_text(env_content, encoding="utf-8")

    # 3. README.md
    readme_content = dedent(f'''\
        # {nombre}

        API REST construida con FastAPI y NoSQL Serverless (Firebase Firestore).

        ## Configuración de Autenticación
        1. **Desarrollo local:** Copia `.env.example` a `.env` y coloca el archivo `serviceAccountKey.json` en la raíz del proyecto.
        2. **Producción / Nube:** Configura las variables de entorno (`FIREBASE_PROJECT_ID`, `FIREBASE_PRIVATE_KEY`, etc.) en la plataforma de hosting.

        ## Ejecución Local
        1. Copia variables de entorno: `cp .env.example .env`
        2. Instala dependencias: `pip install -r requirements.txt`
        3. Inicia la API: `python run.py`
        4. Documentación interactiva en: `http://127.0.0.1:8000/docs`
    ''')
    (target_p / "README.md").write_text(readme_content, encoding="utf-8")