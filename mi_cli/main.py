import os
import json
import sys
import subprocess
import typer
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box
import inquirer

console = Console()
app = typer.Typer()

__version__ = "0.2.0"

def version_callback(value: bool):
    """Muestra la versión de MoldPy y sale."""
    if value:
        console.print(f"[bold cyan]🧱 MoldPy[/bold cyan] versión [bold spring_green1]{__version__}[/bold spring_green1]")
        raise typer.Exit()

@app.callback()
def main_callback(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Muestra la versión instalada de MoldPy.",
        callback=version_callback,
        is_eager=True,
    )
):
    """🧱 MoldPy — Scaffolder de Proyectos en Python"""
    pass

def mostrar_header():
    """Muestra el logo ASCII y banner principal de MoldPy"""
    ascii_logo = (
        "  __  __ Old   _ _____        \n"
        " |  \\/  |  _ \\| |  __ \\       \n"
        " | \\  / | |_) | | |__) | _   _\n"
        " | |\\/| |  _ <| |  ___/ | | | |\n"
        " | |  | | |_) | | |     | |_| |\n"
        " |_|  |_|____/|_|_|      \\__, |\n"
        "                          __/ |\n"
        "                         |___/ "
    )
    console.print(Align.center(f"[bold magenta]{ascii_logo}[/bold magenta]"))
    console.print(
        Panel(
            Align.center("[bold cyan]🧱 MoldPy[/bold cyan] — [italic white]Scaffolder Interactivo de Proyectos[/italic white]"),
            border_style="bright_blue",
            box=box.ROUNDED
        )
    )
    console.print()

def generar_plantilla_fastapi(target_path, nombre, autor):
    app_dir = os.path.join(target_path, "app")
    routers_dir = os.path.join(app_dir, "routers")
    os.makedirs(routers_dir, exist_ok=True)

    with open(os.path.join(app_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'from fastapi import FastAPI\n\n'
            f'app = FastAPI(title="{nombre}")\n\n'
            '@app.get("/")\n'
            'def read_root():\n'
            '    return {"message": "¡API corriendo exitosamente!"}\n'
        )

    with open(os.path.join(routers_dir, "__init__.py"), "w", encoding="utf-8") as f:
        f.write("# Módulo de rutas\n")

    with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f'# {nombre}\n\n'
            '## Ejecutar la API\n'
            '1. Activa tu entorno virtual.\n'
            '2. Corre el servidor con:\n'
            '```bash\n'
            'uvicorn app.main:app --reload\n'
            '```\n'
        )

def generar_plantilla_streamlit(target_path, nombre, autor):
    pages_dir = os.path.join(target_path, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    with open(os.path.join(target_path, "app.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'import streamlit as st\n\n'
            f'st.set_page_config(page_title="{nombre}", page_icon="📊")\n'
            f'st.title("📊 {nombre}")\n'
            'st.write("¡Bienvenido a tu Dashboard!")\n\n'
            'st.sidebar.success("Selecciona una página arriba.")\n'
        )

    with open(os.path.join(pages_dir, "1_Analytics.py"), "w", encoding="utf-8") as f:
        f.write(
            'import streamlit as st\n\n'
            'st.header("Métricas y Analíticas")\n'
            'st.metric(label="Usuarios Activos", value="1,250", delta="+12%")\n'
        )

    with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f'# {nombre}\n\n'
            '## Ejecutar el Dashboard\n'
            '```bash\n'
            'streamlit run app.py\n'
            '```\n'
        )

def generar_plantilla_script(target_path, nombre, autor):
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

def generar_plantilla_datascience(target_path, nombre, autor):
    """NUEVA PLANTILLA: Genera la estructura de archivos para Data Science"""
    data_raw = os.path.join(target_path, "data", "raw")
    data_processed = os.path.join(target_path, "data", "processed")
    notebooks_dir = os.path.join(target_path, "notebooks")
    src_dir = os.path.join(target_path, "src")

    os.makedirs(data_raw, exist_ok=True)
    os.makedirs(data_processed, exist_ok=True)
    os.makedirs(notebooks_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    # Archivo .gitkeep en carpetas vacías de datos
    with open(os.path.join(data_raw, ".gitkeep"), "w") as f:
        pass
    with open(os.path.join(data_processed, ".gitkeep"), "w") as f:
        pass

    # Notebook básico de inicio
    notebook_sample = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {nombre}\n", f"**Autor:** {autor}\n", "\nNotebook de exploración inicial."]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": ["import pandas as pd\n", "import numpy as np\n", "\nprint('¡Entorno de Análisis de Datos listo!')"]
            }
        ],
        "metadata": {
            "language_info": {"name": "python"}
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    with open(os.path.join(notebooks_dir, "01_exploracion.ipynb"), "w", encoding="utf-8") as f:
        json.dump(notebook_sample, f, indent=2)

    # Script src/analysis.py
    with open(os.path.join(src_dir, "analysis.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'import pandas as pd\n\n'
            'def main():\n'
            '    print("Cargando y procesando datos...")\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )

    # README.md
    with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f'# {nombre}\n\n'
            'Proyecto de Análisis de Datos y Data Science.\n\n'
            '## Estructura\n'
            '- `data/raw/`: Datos sin procesar.\n'
            '- `data/processed/`: Datos limpios y procesados.\n'
            '- `notebooks/`: Jupyter Notebooks de análisis.\n'
            '- `src/`: Scripts ejecutables.\n'
        )


@app.command()
def create():
    """Crea un nuevo proyecto de forma interactiva"""
    
    mostrar_header()

    questions = [
        inquirer.List(
            'proyecto',
            message="¿Qué tipo de proyecto quieres crear?",
            choices=[
                'API REST en FastAPI',
                'Script de Automatización',
                'Dashboard con Streamlit',
                'Data Science (Pandas & Jupyter)'  # Nueva opción agregada
            ],
        ),
        inquirer.Text(
            'nombre',
            message="¿Nombre de la carpeta del proyecto?",
            default="mi-proyecto-python"
        ),
        inquirer.Text(
            'autor',
            message="¿Nombre del autor?",
            default="Desarrollador"
        ),
        inquirer.Confirm(
            'git',
            message="¿Inicializar .gitignore?",
            default=True
        ),
        inquirer.Confirm(
            'instalar',
            message="¿Deseas crear el venv e instalar dependencias?",
            default=True
        ),
    ]

    answers = inquirer.prompt(questions)
    
    if not answers:
        console.print("[red]Proceso cancelado.[/red]")
        raise typer.Exit()

    proyecto = answers['proyecto']
    nombre = answers['nombre']
    autor = answers['autor']
    git = answers['git']
    instalar = answers['instalar']

    console.print()
    table = Table(
        title="📋 Resumen de Configuración — MoldPy",
        box=box.ROUNDED,
        header_style="bold magenta",
        border_style="bright_blue"
    )
    table.add_column("Parámetro", style="cyan", justify="right", width=25)
    table.add_column("Valor Elegido", style="spring_green1", justify="left")

    table.add_row("Tipo de Proyecto", proyecto)
    table.add_row("Carpeta / Directorio", nombre)
    table.add_row("Autor", autor)
    table.add_row("Incluir .gitignore", "Sí" if git else "No")
    table.add_row("Crear venv e instalar", "Sí" if instalar else "No")

    console.print(table)
    console.print()

    confirmacion = inquirer.confirm("¿Deseas continuar y crear el proyecto?", default=True)

    if not confirmacion:
        console.print("[yellow]⚠ Operación cancelada por el usuario. No se crearon archivos.[/yellow]\n")
        raise typer.Exit()

    target_path = os.path.join(os.getcwd(), nombre)

    with console.status(f"[bold yellow]Generando estructura para '{proyecto}'...[/bold yellow]", spinner="aesthetic"):
        os.makedirs(target_path, exist_ok=True)

        req_path = os.path.join(target_path, "requirements.txt")
        with open(req_path, "w", encoding="utf-8") as f:
            f.write(f"# Creado por: {autor}\n")
            if "FastAPI" in proyecto:
                f.write("fastapi\nuvicorn[standard]\n")
            elif "Streamlit" in proyecto:
                f.write("streamlit\n")
            elif "Data Science" in proyecto:
                f.write("pandas\nnumpy\njupyterlab\nmatplotlib\n")
            else:
                f.write("requests\npython-dotenv\n")

        if "FastAPI" in proyecto:
            generar_plantilla_fastapi(target_path, nombre, autor)
        elif "Streamlit" in proyecto:
            generar_plantilla_streamlit(target_path, nombre, autor)
        elif "Data Science" in proyecto:
            generar_plantilla_datascience(target_path, nombre, autor)
        else:
            generar_plantilla_script(target_path, nombre, autor)

        if git:
            gitignore_path = os.path.join(target_path, ".gitignore")
            with open(gitignore_path, "w", encoding="utf-8") as f:
                f.write("__pycache__/\n*.pyc\nvenv/\n.env\n.vscode/\n.ipynb_checkpoints/\ndata/raw/*\n!data/raw/.gitkeep\n")

    if instalar:
        venv_path = os.path.join(target_path, "venv")
        
        with console.status("[bold yellow]Creando entorno virtual (venv)...[/bold yellow]", spinner="bouncingBar"):
            try:
                subprocess.run(
                    [sys.executable, "-m", "venv", venv_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                console.print("[bold green]✔ Entorno virtual (venv) creado exitosamente.[/bold green]")
            except subprocess.CalledProcessError:
                console.print("[bold red]✖ Error al crear el entorno virtual.[/bold red]")

        pip_executable = os.path.join(venv_path, "Scripts", "pip.exe") if os.name == 'nt' else os.path.join(venv_path, "bin", "pip")

        with console.status("[bold yellow]Instalando dependencias de requirements.txt con pip...[/bold yellow]", spinner="dots"):
            try:
                subprocess.run(
                    [pip_executable, "install", "-r", req_path],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                console.print("[bold green]✔ Dependencias instaladas correctamente.[/bold green]")
            except subprocess.CalledProcessError:
                console.print("[bold red]✖ Error al instalar las dependencias con pip.[/bold red]")

    console.print(f"\n[bold spring_green1]✔ ¡Proyecto '{nombre}' creado con éxito por MoldPy! 🎉[/bold spring_green1]")
    console.print(f"[dim]Ubicación: {target_path}[/dim]\n")

if __name__ == "__main__":
    app()