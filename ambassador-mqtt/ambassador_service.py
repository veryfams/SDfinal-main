from fastapi import FastAPI
from mqtt_ambassador import MQTTAmbassador
import uvicorn
import asyncio
import threading
import os

app = FastAPI(title="MQTT Ambassador Service", version="1.0.0")

# Inicializar ambassador
mqtt_ambassador = MQTTAmbassador(
    broker_host=os.getenv("MQTT_HOST", "mosquitto"),
    broker_port=int(os.getenv("MQTT_PORT", 1883)),
    client_id=f"ambassador-{os.getenv('HOSTNAME', 'unknown')}"
)

@app.on_event("startup")
async def startup_event():
    """Conectar ambassador al iniciar"""
    def connect_mqtt():
        mqtt_ambassador.connect()
        
    # Ejecutar conexión MQTT en hilo separado
    mqtt_thread = threading.Thread(target=connect_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    metrics = mqtt_ambassador.get_metrics()
    return {
        "status": "healthy" if metrics['successful_connections'] > 0 else "unhealthy",
        "service": "mqtt_ambassador",
        "metrics": metrics
    }

@app.get("/metrics")
async def get_metrics():
    """Endpoint para métricas del ambassador"""
    return mqtt_ambassador.get_metrics()

@app.post("/publish/{topic}")
async def publish_message(topic: str, payload: dict):
    """Endpoint para publicar mensajes a través del ambassador"""
    import json
    success = mqtt_ambassador.publish(topic, json.dumps(payload))
    return {"published": success, "topic": topic}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
