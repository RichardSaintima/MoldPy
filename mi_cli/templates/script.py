import os

def generar_plantilla_script(target_path: str, nombre: str, autor: str):
    """Genera la estructura para un Script de automatización."""
    src_dir = os.path.join(target_path, "src")
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(src_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'import os\n'
            'from dotenv import load_dotenv\n\n'
            'load_dotenv()\n\n'
            'def run():\n'
            '    api_key = os.getenv("API_KEY", "no_key")\n'
            '    print(f"Iniciando automatización para {nombre}...")\n'
            '    print(f"API Key configurada: {api_key}")\n\n'
            'if __name__ == "__main__":\n'
            '    run()\n'
        )

    with open(os.path.join(target_path, ".env.example"), "w", encoding="utf-8") as f:
        f.write("API_KEY=tu_clave_aqui\nDEBUG=True\n")