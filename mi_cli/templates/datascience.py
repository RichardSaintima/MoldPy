import os
import json

def generar_plantilla_datascience(target_path: str, nombre: str, autor: str):
    """Genera la estructura de archivos para Data Science."""
    data_raw = os.path.join(target_path, "data", "raw")
    data_processed = os.path.join(target_path, "data", "processed")
    notebooks_dir = os.path.join(target_path, "notebooks")
    src_dir = os.path.join(target_path, "src")

    os.makedirs(data_raw, exist_ok=True)
    os.makedirs(data_processed, exist_ok=True)
    os.makedirs(notebooks_dir, exist_ok=True)
    os.makedirs(src_dir, exist_ok=True)

    with open(os.path.join(data_raw, ".gitkeep"), "w") as f:
        pass
    with open(os.path.join(data_processed, ".gitkeep"), "w") as f:
        pass

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

    with open(os.path.join(src_dir, "analysis.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'import pandas as pd\n\n'
            'def main():\n'
            '    print("Cargando y procesando datos...")\n\n'
            'if __name__ == "__main__":\n'
            '    main()\n'
        )

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