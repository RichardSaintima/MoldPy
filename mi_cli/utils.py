import os
import sys
import subprocess
from rich.console import Console

console = Console()

def crear_gitignore(target_path: str) -> str:
    """Crea un archivo .gitignore estándar para Python."""
    gitignore_path = os.path.join(target_path, ".gitignore")
    content = (
        "__pycache__/\n"
        "*.py[cod]\n"
        "*$py.class\n\n"
        "venv/\n"
        "env/\n"
        "ENV/\n\n"
        ".env\n"
        "*.db\n"
        "*.sqlite3\n\n"
        ".vscode/\n"
        ".idea/\n"
    )
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write(content)
    return gitignore_path


def instalar_entorno_virtual(target_path: str, req_path: str):
    """Crea el entorno virtual e instala las dependencias mediante pip."""
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