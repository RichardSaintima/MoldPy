import os
import pytest
from mi_cli.utils import crear_gitignore

def test_crear_gitignore(tmp_path):
    target_path = str(tmp_path)
    crear_gitignore(target_path)

    gitignore_path = tmp_path / ".gitignore"
    assert gitignore_path.exists()
    content = gitignore_path.read_text(encoding="utf-8")
    assert "venv/" in content
    assert ".env" in content
    assert "__pycache__/" in content