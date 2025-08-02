# 1. Imagen base ligera
FROM python:3.11-slim

# 2. Variables para optimizar Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Carpeta de trabajo
WORKDIR /app

# 4. Instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt



# 5. Copia el código de la app
COPY . .

# 6. Expone el puerto interno (80) y levanta Uvicorn
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
