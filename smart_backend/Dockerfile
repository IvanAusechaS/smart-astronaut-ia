FROM python:3.11-slim

WORKDIR /app

# Copiar requirements y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto (Render usa la variable de entorno PORT)
EXPOSE 8000

# Comando para iniciar la aplicación
# En producción, usa el puerto de la variable de entorno PORT
CMD uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
