FROM python:3.11-slim

# Evita escribir archivos .pyc y mejora logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instala solo dependencias primero
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia solo el código necesario
COPY app/ ./app

# Expone el puerto de la API
EXPOSE 8000

# Comando de arranque
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]