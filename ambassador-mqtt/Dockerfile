FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del ambassador
COPY mqtt_ambassador.py .
COPY ambassador_service.py .

# Crear directorio para logs
RUN mkdir -p /var/log/mqtt

# Exponer puerto para métricas/health check
EXPOSE 8080

CMD ["python", "ambassador_service.py"]
