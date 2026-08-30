import os
import json
import pytest

from mi_cli.templates.fastapi import generar_plantilla_fastapi
from mi_cli.templates.streamlit import generar_plantilla_streamlit
from mi_cli.templates.datascience import generar_plantilla_datascience
from mi_cli.templates.script import generar_plantilla_script
from mi_cli.templates.fastapi_sqlmodel import generar_plantilla_fastapi_sqlmodel
from mi_cli.templates.fastapi_firebase import generar_plantilla_fastapi_firebase


def test_generar_plantilla_fastapi(tmp_path):
    target_dir = tmp_path / "mi_api"
    target_path = str(target_dir)

    generar_plantilla_fastapi(target_path, "mi_api", "DevTest")

    assert target_dir.exists()
    assert (target_dir / "app" / "main.py").exists()
    assert (target_dir / "app" / "routers" / "__init__.py").exists()
    assert (target_dir / "run.py").exists()
    assert (target_dir / "README.md").exists()

    main_content = (target_dir / "app" / "main.py").read_text(encoding="utf-8")
    assert "Creado por DevTest" in main_content
    assert 'title="mi_api"' in main_content


def test_generar_plantilla_fastapi_sqlmodel(tmp_path):
    target_dir = tmp_path / "mi_api_sqlmodel"
    target_path = str(target_dir)

    generar_plantilla_fastapi_sqlmodel(target_path, "mi_api_sqlmodel", "DevTest")

    assert (target_dir / "app" / "database.py").exists()
    assert (target_dir / "app" / "models" / "item.py").exists()
    assert (target_dir / "app" / "routers" / "items.py").exists()
    assert (target_dir / "run.py").exists()
    assert (target_dir / ".env.example").exists()

    db_content = (target_dir / "app" / "database.py").read_text(encoding="utf-8")
    assert "SQLModel" in db_content



def test_generar_plantilla_fastapi_firebase(tmp_path):
    target_dir = tmp_path / "mi_api_firebase"
    target_path = str(target_dir)

    generar_plantilla_fastapi_firebase(target_path, "mi_api_firebase", "DevTest")

    assert (target_dir / "app" / "database.py").exists()
    assert (target_dir / "app" / "routers" / "items.py").exists()
    assert (target_dir / "run.py").exists()
    assert (target_dir / ".env.example").exists()

    db_content = (target_dir / "app" / "database.py").read_text(encoding="utf-8")
    assert "firebase_admin" in db_content


def test_generar_plantilla_streamlit(tmp_path):
    target_dir = tmp_path / "mi_dashboard"
    target_path = str(target_dir)

    generar_plantilla_streamlit(target_path, "mi_dashboard", "DevTest")

    assert (target_dir / "app.py").exists()
    assert (target_dir / "pages" / "1_Analytics.py").exists()
    assert (target_dir / "README.md").exists()

    app_content = (target_dir / "app.py").read_text(encoding="utf-8")
    assert 'st.title("📊 mi_dashboard")' in app_content


def test_generar_plantilla_datascience(tmp_path):
    target_dir = tmp_path / "mi_ds"
    target_path = str(target_dir)

    generar_plantilla_datascience(target_path, "mi_ds", "DevTest")

    assert (target_dir / "data" / "raw" / ".gitkeep").exists()
    assert (target_dir / "data" / "processed" / ".gitkeep").exists()
    assert (target_dir / "src" / "analysis.py").exists()

    notebook_path = target_dir / "notebooks" / "01_exploracion.ipynb"
    assert notebook_path.exists()

    with open(notebook_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)
        assert nb_data["nbformat"] == 4
        assert "DevTest" in nb_data["cells"][0]["source"][1]


def test_generar_plantilla_script(tmp_path):
    target_dir = tmp_path / "mi_script"
    target_path = str(target_dir)

    generar_plantilla_script(target_path, "mi_script", "DevTest")

    assert (target_dir / "src" / "main.py").exists()
    assert (target_dir / ".env.example").exists()

    env_content = (target_dir / ".env.example").read_text(encoding="utf-8")
    assert "API_KEY=tu_clave_aqui" in env_content