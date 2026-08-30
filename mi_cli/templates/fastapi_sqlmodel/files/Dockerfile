FROM python:3.11-slim

# 1. Actualizar paquetes del sistema para mitigar vulnerabilidades C/H/M/L
RUN apt-get update && apt-get upgrade -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 3. Crear usuario no-root para seguridad (SonarQube S6471)
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

COPY . .

# Cambiar el propietario de los archivos copiados
RUN chown -R appuser:appuser /app

# 4. Cambiar al usuario sin privilegios
USER appuser

EXPOSE 8000

CMD ["python", "run.py"]