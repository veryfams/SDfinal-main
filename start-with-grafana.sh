#!/bin/bash

echo "🚀 Iniciando ADN Alert System con Grafana Logging"
echo "================================================="

# Verificar que Docker esté ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose. Inicia Docker primero."
    exit 1
fi

echo "📦 Construyendo imágenes..."
docker-compose build

echo "🔄 Iniciando servicios..."
docker-compose up -d

echo "⏳ Esperando que los servicios estén listos..."
sleep 15

echo "✅ Sistema iniciado!"
echo ""
echo "🌐 URLs disponibles:"
echo "   - Sistema Principal: http://localhost:8000"
echo "   - Frontend React:    http://localhost:3000"
echo "   - Grafana:           http://localhost:3001"
echo "   - Backend 1:         http://localhost:8001"
echo "   - Backend 2:         http://localhost:8002"
echo ""
echo "🔑 Credenciales Grafana:"
echo "   - Usuario: admin"
echo "   - Contraseña: admin123"
echo ""
echo "📊 Dashboard de logs estará disponible en Grafana"
echo "🔍 Para ver logs en tiempo real: ./scripts/log-monitor.sh tail"
