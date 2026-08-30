# Entorno de Desarrollo Local

## Activar el entorno virtual (Windows PowerShell)

```bash
.\venv\Scripts\Activate.ps1
```

## Instalar el proyecto en modo editable (los cambios se aplican al instante)

```bash
pip install -e .
```

## Probar tu CLI localmente

```bash
moldpy --version
```

```bash
moldpy create
```

# Pruebas Automatizadas (pytest)

## Instalar pytest si no lo tienes

```bash
pip install pytest
```

## Ejecutar todos los tests unitarios

```bash
pytest
```

# Proceso de Construcción y Empaquetado (Build)

## Instalar las herramientas oficiales de empaquetado

```bash
pip install --upgrade build twine
```

## Limpiar compilaciones antiguas (Windows PowerShell)

```bash
Remove-Item -Recurse -Force dist/, build/, *.egg-info -ErrorAction SilentlyContinue
```

## Compilar el paquete (genera los archivos .whl y .tar.gz en la carpeta /dist)

```bash
python -m build
```

# Publicación Manual a PyPI

## 1. Verificar que los paquetes generados en /dist no tengan errores

```bash
python -m twine check dist/*
```

## 2. Subir a TestPyPI (Servidor de pruebas - Opcional pero recomendado)

```bash
python -m twine upload --repository testpypi dist/*
```

## 3. Subir a PyPI Oficial (Producción)

```bash
python -m twine upload dist/*
```

# Flujo Estándar con Git

## Ver estado de los archivos cambiados

```bash
git status
```

## Agregar todos los cambios

```bash
git add .
```

## Crear commit de la versión

```bash
git commit -m "Release v0.2.2: Modular structure, tests, and CI/CD workflow"
```

## Subir a GitHub

```bash
git push origin main
```
