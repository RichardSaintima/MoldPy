import pytest
from typer.testing import CliRunner
from mi_cli.main import app

runner = CliRunner()


def test_version_flag():
    # Ejecuta el comando 'moldpy --version'
    result = runner.invoke(app, ["--version"])

    # Verifica que el código de salida sea 0 (éxito) y contenga la versión
    assert result.exit_code == 0
    assert "MoldPy" in result.stdout
    assert "0.2.2" in result.stdout