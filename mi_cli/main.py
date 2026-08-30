import os
import sys
import subprocess
import typer
from rich.console import Console

from mi_cli.ui import mostrar_header, obtener_respuestas_usuario
from mi_cli.utils import crear_gitignore
from mi_cli.templates.fastapi import generar_plantilla_fastapi
from mi_cli.templates.fastapi_sqlmodel import generar_plantilla_fastapi_sqlmodel
from mi_cli.templates.fastapi_firebase import generar_plantilla_fastapi_firebase
from mi_cli.templates.fastapi_supabase import generar_plantilla_fastapi_supabase
from mi_cli.templates.streamlit import generar_plantilla_streamlit
from mi_cli.templates.datascience import generar_plantilla_datascience
from mi_cli.templates.script import generar_plantilla_script

app = typer.Typer()
console = Console()

__version__ = "0.2.1"


def version_callback(value: bool):
    if value:
        console.print(
            f"[bold cyan]MoldPy CLI[/bold cyan] versión: [bold green]{__version__}[/bold green]")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Muestra la versión de MoldPy CLI",
        callback=version_callback,
        is_eager=True,
    )
):
    """MoldPy - Scaffolder Interactivo de Proyectos Python"""
    pass


@app.command()
def create():
    try:
        mostrar_header()
        answers = obtener_respuestas_usuario()

        if not answers:
            console.print("[red]Proceso cancelado por el usuario.[/red]")
            raise typer.Exit()

        nombre = answers['nombre']
        autor = answers['autor']
        proyecto = answers['proyecto']
        crear_venv = answers['crear_venv']

        target_path = os.path.join(os.getcwd(), nombre)

        if os.path.exists(target_path):
            console.print(
                f"[bold red]Error:[/bold red] La carpeta '[yellow]{nombre}[/yellow]' ya existe.")
            raise typer.Exit()

        os.makedirs(target_path, exist_ok=True)

        with console.status("[bold green]Generando la estructura del proyecto...", spinner="dots"):
            # 1. FastAPI + SQLModel
            if "SQLModel" in proyecto:
                generar_plantilla_fastapi_sqlmodel(target_path, nombre, autor)

            # 2. FastAPI + Serverless (Evaluación corregida)
            elif "Backend Serverless" in proyecto or "NoSQL" in proyecto:
                proveedor = answers.get(
                    "proveedor_serverless", "Firebase Firestore")
                if "Firebase" in proveedor:
                    generar_plantilla_fastapi_firebase(target_path, nombre, autor)
                elif "Supabase" in proveedor:
                    generar_plantilla_fastapi_supabase(target_path, nombre, autor)

            # 3. FastAPI Básica (Debe ir al final de las opciones con FastAPI)
            elif "FastAPI" in proyecto:
                generar_plantilla_fastapi(target_path, nombre, autor)

            elif "Streamlit" in proyecto:
                generar_plantilla_streamlit(target_path, nombre, autor)
            elif "Data Science" in proyecto:
                generar_plantilla_datascience(target_path, nombre, autor)
            elif "Script" in proyecto:
                generar_plantilla_script(target_path, nombre, autor)

            crear_gitignore(target_path)

        console.print(
            f"✨ ¡Proyecto [bold cyan]{nombre}[/bold cyan] creado exitosamente!")

        if crear_venv:
            with console.status("[bold blue]Creando el entorno virtual (venv)...", spinner="earth"):
                venv_dir = os.path.join(target_path, "venv")
                subprocess.run(
                    [sys.executable, "-m", "venv", venv_dir], check=True)
            console.print(
                "📦 Entorno virtual [bold green]venv[/bold green] creado con éxito.")

        console.print("\n[bold yellow]Próximos pasos:[/bold yellow]")
        console.print(f"  1. [cyan]cd {nombre}[/cyan]")
        if crear_venv:
            if sys.platform == "win32":
                console.print("  2. [cyan].\\venv\\Scripts\\activate[/cyan]")
            else:
                console.print("  2. [cyan]source venv/bin/activate[/cyan]")
            console.print("  3. [cyan]pip install -r requirements.txt[/cyan]")
        else:
            console.print("  2. [cyan]pip install -r requirements.txt[/cyan]")

        if "FastAPI" in proyecto or "NoSQL Serverless" in proyecto:
            console.print("  4. [cyan]python run.py[/cyan]")

    except KeyboardInterrupt:
        console.print(
            "\n[yellow]⚠ Operación cancelada por el usuario.[/yellow]\n")
        raise typer.Exit()


if __name__ == "__main__":
    app()
