#!/bin/bash

echo "🔍 Monitor de Logs del Sistema ADN Alert"
echo "========================================"

LOG_DIR="/shared/logs/consolidated"

# Función para mostrar logs en tiempo real
tail_logs() {
    echo "📊 Mostrando logs en tiempo real..."
    echo "Presiona Ctrl+C para salir"
    echo "----------------------------------------"
    
    # Tail de todos los archivos de log
    tail -f ${LOG_DIR}/adn-alert-system*.log 2>/dev/null | while read line; do
        echo "[$(date '+%H:%M:%S')] $line"
    done
}

# Función para buscar en logs
search_logs() {
    if [ -z "$1" ]; then
        echo "❌ Uso: search_logs <término_de_búsqueda>"
        return 1
    fi
    
    echo "🔍 Buscando '$1' en los logs..."
    echo "----------------------------------------"
    
    grep -r "$1" ${LOG_DIR}/ --color=always 2>/dev/null || echo "No se encontraron resultados"
}

# Función para mostrar estadísticas
show_stats() {
    echo "📈 Estadísticas de Logs"
    echo "----------------------------------------"
    
    if [ -d "$LOG_DIR" ]; then
        echo "📁 Directorio de logs: $LOG_DIR"
        echo "📊 Archivos de log:"
        ls -lh ${LOG_DIR}/ 2>/dev/null | grep -v total
        echo ""
        echo "📈 Líneas por servicio (últimas 1000 líneas):"
        
        # Contar líneas por servicio
        tail -n 1000 ${LOG_DIR}/adn-alert-system*.log 2>/dev/null | \
        grep -o '"service_name":"[^"]*"' | \
        sort | uniq -c | \
        while read count service; do
            service_clean=$(echo $service | sed 's/"service_name":"\([^"]*\)"/\1/')
            echo "  - $service_clean: $count mensajes"
        done
    else
        echo "❌ Directorio de logs no encontrado: $LOG_DIR"
    fi
}

# Función para mostrar alertas recientes
show_recent_alerts() {
    echo "🚨 Alertas Recientes (últimas 50)"
    echo "----------------------------------------"
    
    tail -n 50 ${LOG_DIR}/adn-alert-system*.log 2>/dev/null | \
    grep -i "alerta\|alert\|error\|warning" --color=always | \
    tail -n 20
}

# Menú principal
case "$1" in
    "tail"|"follow"|"-f")
        tail_logs
        ;;
    "search"|"-s")
        search_logs "$2"
        ;;
    "stats"|"-st")
        show_stats
        ;;
    "alerts"|"-a")
        show_recent_alerts
        ;;
    "help"|"-h"|"")
        echo "🔧 Comandos disponibles:"
        echo "  $0 tail        - Ver logs en tiempo real"
        echo "  $0 search <término> - Buscar en logs"
        echo "  $0 stats       - Mostrar estadísticas"
        echo "  $0 alerts      - Mostrar alertas recientes"
        echo "  $0 help        - Mostrar esta ayuda"
        ;;
    *)
        echo "❌ Comando desconocido: $1"
        echo "Usa '$0 help' para ver comandos disponibles"
        exit 1
        ;;
esac
