import inquirer
import rich
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich import box

console = Console()

def mostrar_header():
    """Muestra el logo ASCII y el banner principal de MoldPy."""
    ascii_logo = r"""
  __  __  ____  _     ____  ____  __   __
 |  \/  |/ __ \| |   |  _ \|  _ \ \ \ / /
 | \  / | |  | | |   | | | | |_) | \ V / 
 | |\/| | |  | | |___| |_| |  __/   | |  
 |_|  |_|\____/|_____|____/|_|      |_|  
"""
    console.print(Align.center(f"[bold magenta]{ascii_logo}[/bold magenta]"))
    console.print(
        Panel(
            Align.center("[bold cyan]🧱 MoldPy[/bold cyan] — [italic white]Scaffolder Interactivo de Proyectos[/italic white]"),
            border_style="bright_blue",
            box=box.ROUNDED
        )
    )
    console.print()

def obtener_respuestas_usuario():
    """Lanza el cuestionario interactivo en la terminal."""
    questions = [
        inquirer.List(
            'proyecto',
            message="¿Qué tipo de proyecto quieres crear?",
            choices=[
                'API REST en FastAPI (Básica)',
                'API REST en FastAPI + SQLModel (SQL)',
                'API REST en FastAPI + Backend Serverless'
            ]
        ),
        inquirer.Text('nombre', message="¿Cómo se llamará el proyecto?", default="mi_proyecto"),
        inquirer.Text('autor', message="¿Nombre del Autor/Desarrollador?", default="Desarrollador"),
        inquirer.Confirm('crear_venv', message="¿Deseas crear un entorno virtual (venv)?", default=True),
    ]
    
    console.print(
        Align.center("[dim]Presiona [bold]Ctrl + C[/bold] en cualquier momento para cancelar.[/dim]")
    )
    console.print()
    
    respuestas = inquirer.prompt(questions)
    if not respuestas:
        return None

    # Pregunta adicional si el usuario elige Backend Serverless
    if respuestas['proyecto'] == 'API REST en FastAPI + Backend Serverless':
        sub_questions = [
            inquirer.List(
                'proveedor_serverless',
                message="Selecciona el proveedor Serverless:",
                choices=[
                    'Firebase Firestore',
                    'Supabase'
                ]
            )
        ]
        sub_respuestas = inquirer.prompt(sub_questions)
        if not sub_respuestas:
            return None
        respuestas['proveedor_serverless'] = sub_respuestas['proveedor_serverless']

    return respuestas