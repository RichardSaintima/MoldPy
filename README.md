# 🧱 MoldPy

> Scaffolder e inicializador interactivo de proyectos en Python.

**MoldPy** es una herramienta de línea de comandos (CLI) diseñada para maquetar la estructura inicial de proyectos en Python (APIs en FastAPI, Dashboards en Streamlit, Data Science y Scripts de automatización) con configuración automática de entornos virtuales (`venv`), `.gitignore` y dependencias.

---

## 🎨 Características

- 🚀 **Plantillas Listas:** Genera proyectos completos para **FastAPI**, **Streamlit**, **Data Science** o **Scripts**.
- 🛠️ **Entornos Virtuales:** Crea el `venv` e instala las dependencias de `requirements.txt` automáticamente en segundo plano.
- 📋 **Previsualización Clara:** Tabla interactiva con el resumen de la configuración antes de escribir en disco.
- 💅 **Interfaz Moderna:** Diseñada con banderas y colores tipo terminal *cyberpunk*.

---

## 📦 Instalación

Elige el método de instalación que prefieras:

### Opción A: Con `pipx` (Recomendado para la mayoría)

Instala `moldpy` como una herramienta global independiente sin necesidad de crear entornos virtuales manuales:

```bash
pip install pipx
```

```bash
pipx install moldpy
```

### Opción B: Con `pip` (Instalación clásica)

Si prefieres usar `pip` directamente, **debes crear y activar primero tu propio entorno virtual (venv) para evitar problemas de permisos** con el Python del sistema:

### Crea y activa un entorno virtual

- Crear el entorno

```bash
python -m venv venv
```

- Activar en Windows (PowerShell)

```bash
.\venv\Scripts\activate
```

- Activar en Linux / macOS

```bash
source venv/bin/activate
```

### Para verificar que se instaló correctamente

```bash
moldpy --version
```

## 🚀 Guía de Uso Paso a Paso

- **Iniciar el Creador de Proyectos**
  Abre la terminal en la carpeta donde quieras crear tu nuevo proyecto y ejecuta:

```bash
moldpy create
```

- **Responder a las Preguntas del Asistente**
MoldPy te guiará con un menú interactivo:
    1. Tipo de proyecto: Elige entre:
        ⚡ API REST en FastAPI (Estructura de API con servidor Uvicorn).
        📊 Dashboard con Streamlit (Interfaz web interactiva para datos).
        📈 Data Science (Pandas & Jupyter) (Estructura para datos con notebooks y carpetas de datos).
        🛠️ Script de Automatización (Base limpia para automatización con .env).
    2. Nombre de la carpeta: El nombre del directorio donde se creará el código.
    3. Autor: Tu nombre o marca personal.
    4. Entorno Virtual (venv): Opción para crear el entorno e instalar dependencias automáticamente.

## 🛠️ Comandos Disponibles

| Comando | Descripción |
| :--- | :--- |
| `moldpy create` | Inicia el asistente interactivo de creación. |
| `moldpy --version` o `moldpy -v` | Muestra la versión actual instalada de MoldPy. |
| `moldpy --help` | Muestra la ayuda general y opciones disponibles. |

## 💻 Pasos Finales para Usar tu Proyecto Generado

**Una vez que MoldPy termine de crear tu proyecto, sigue estos pasos para empezar a trabajar:**

- **Entra a la carpeta generada**:

```bash
cd mi-app
```

- **Activa el Entorno Virtual (venv):**

Windows (PowerShell):
    PowerShell

```bash
.\venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

-**Ejecuta tu proyecto**

```bash
python run.py
```

1. ¿Qué hace MoldPy automáticamente por ti?

- Te hace unas preguntas interactivas (tipo de proyecto, nombre, autor, etc.).**

- Crea la carpeta de tu nuevo proyecto (por ejemplo: mi-api).

- Genera un venv interno dentro de mi-api/venv exclusivo para las librerías de tu nueva aplicación **(FastAPI, Streamlit, etc.)** e instala sus dependencias automáticamente.
