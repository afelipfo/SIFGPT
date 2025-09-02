# Dockerfile para TUNRAG
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Crear directorios necesarios
RUN mkdir -p logs input/audios

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash tunrag && \
    chown -R tunrag:tunrag /app
USER tunrag

# Exponer puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV PYTHONPATH=/app/src
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Comando de inicio
CMD ["python", "app.py"]
