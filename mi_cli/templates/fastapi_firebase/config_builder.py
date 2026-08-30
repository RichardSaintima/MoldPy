import os


def crear_config_files(app_dir: str, target_path: str, nombre: str):
    """Genera app/config.py, .env.example y README.md para NoSQL Serverless (Firebase)."""

    # 1. app/config.py
    with open(os.path.join(app_dir, "config.py"), "w", encoding="utf-8") as f:
        f.write(
            "import os\n"
            "from dotenv import load_dotenv\n\n"
            "load_dotenv()\n\n"
            "# Configuración CORS\n"
            'CORS_ORIGINS_RAW = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000")\n'
            'CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGINS_RAW.split(",") if origin.strip()]\n\n'
            "# Ruta de credenciales Firebase/Firestore (Desarrollo local)\n"
            'FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")\n'
        )

    # 2. .env.example con opciones de desarrollo y producción
    with open(
        os.path.join(target_path, ".env.example"), "w", encoding="utf-8"
    ) as f:
        f.write(
            "# Configuración CORS\n"
            "CORS_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:8000\n\n"
            "# OPCIÓN A: Archivo local (Para desarrollo local)\n"
            "FIREBASE_CREDENTIALS_PATH=serviceAccountKey.json\n\n"
            "# OPCIÓN B: Variables de entorno individuales (Para producción/nube sin subir archivos)\n"
            "# FIREBASE_PROJECT_ID=tu-proyecto-id\n"
            "# FIREBASE_PRIVATE_KEY_ID=clave-id\n"
            '# FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"\n'
            "# FIREBASE_CLIENT_EMAIL=firebase-adminsdk@tu-proyecto.iam.gserviceaccount.com\n"
            "# FIREBASE_CLIENT_ID=123456789\n"
        )

    # 3. README.md
    with open(
        os.path.join(target_path, "README.md"), "w", encoding="utf-8"
    ) as f:
        f.write(
            f"# {nombre}\n\n"
            "API REST construida con FastAPI y NoSQL Serverless (Firebase Firestore).\n\n"
            "## Opciones de Autenticación\n"
            "1. **Desarrollo local:** Coloca `serviceAccountKey.json` en la raíz del proyecto.\n"
            "2. **Producción / Nube:** Configura las variables de entorno (`FIREBASE_PROJECT_ID`, `FIREBASE_PRIVATE_KEY`, etc.) en el servidor de despliegue.\n\n"
            "## Ejecución Local\n"
            "1. Copia `.env.example` a `.env`: `cp .env.example .env`\n"
            "2. Instala dependencias: `pip install -r requirements.txt`\n"
            "3. Inicia la API: `python run.py`\n"
            "4. Documentación interactiva en `http://127.0.0.1:8000/docs`\n"
        )