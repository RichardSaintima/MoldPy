import os

def generar_plantilla_streamlit(target_path: str, nombre: str, autor: str):
    """Genera la estructura de archivos para un Dashboard con Streamlit."""
    pages_dir = os.path.join(target_path, "pages")
    os.makedirs(pages_dir, exist_ok=True)

    with open(os.path.join(target_path, "app.py"), "w", encoding="utf-8") as f:
        f.write(
            f'# Creado por {autor}\n'
            'import streamlit as st\n\n'
            f'st.set_page_config(page_title="{nombre}", page_icon="📊")\n'
            f'st.title("📊 {nombre}")\n'
            'st.write("¡Bienvenido a tu Dashboard!")\n\n'
            'st.sidebar.success("Selecciona una página arriba.")\n'
        )

    with open(os.path.join(pages_dir, "1_Analytics.py"), "w", encoding="utf-8") as f:
        f.write(
            'import streamlit as st\n\n'
            'st.header("Métricas y Analíticas")\n'
            'st.metric(label="Usuarios Activos", value="1,250", delta="+12%")\n'
        )

    with open(os.path.join(target_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(
            f'# {nombre}\n\n'
            '## Ejecutar el Dashboard\n'
            '```bash\n'
            'streamlit run app.py\n'
            '```\n'
        )