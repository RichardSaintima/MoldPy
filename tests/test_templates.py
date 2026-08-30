import os
import json
import pytest

from mi_cli.templates.fastapi import generar_plantilla_fastapi
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