from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from typing import Optional
from enum import Enum
from websocket_manager import WebSocketManager
from mqtt_client import MQTTClient
from db import Database
import asyncio
import os
import socket
import json

app = FastAPI(
    title="Sistema Distribuido de Alerta de Desastres",
    description="Backend FastAPI con WebSocket, MQTT y PostgreSQL",
    version="1.0.0"
)

# Base de datos
db = Database(
    dbname=os.getenv("DB_NAME", "adn_alert_db"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "contraseña"),
    host=os.getenv("DB_HOST", "postgres"),
    port=int(os.getenv("DB_PORT", 5432))
)

# WebSocket manager
ws_manager = WebSocketManager()

# 🔁 MQTT Broker desde el host (no entre contenedores)
mqtt = MQTTClient("host.docker.internal", 1883, "alertas/general", db)

# Manejador al recibir alerta MQTT
def manejar_mensaje(topic, payload, timestamp):
    try:
        alerta = json.loads(payload)
        alerta["hora"] = timestamp.isoformat()
        print("📤 Enviando alerta por WebSocket:", alerta)
        asyncio.run(ws_manager.broadcast(alerta))
    except Exception as e:
        print("❌ Error al procesar o enviar alerta:", e)

mqtt.set_on_message_callback(manejar_mensaje)
mqtt.start()
print("🚀 Cliente MQTT iniciado")


# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    hostname = socket.gethostname()
    print(f"👤 Cliente WebSocket intentando conectar al backend {hostname}...")
    await ws_manager.connect(websocket)
    print(f"✅ Cliente WebSocket conectado al backend {hostname}.")
    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print("❌ Cliente WebSocket desconectado.")
        await ws_manager.disconnect(websocket)


# Endpoints REST

class OrderOptions(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/alertas", summary="Obtener alertas filtradas", tags=["Alertas"])
def get_alertas(
    region: Optional[str] = Query(None),
    tipo: Optional[str] = Query(None),
    mensaje: Optional[str] = Query(None),
    limit: Optional[int] = Query(None, ge=1, le=100),
    offset: Optional[int] = Query(None, ge=0),
    order: Optional[OrderOptions] = Query(OrderOptions.desc)
):
    alertas = db.get_alerts_filtered(region=region, tipo=tipo, mensaje=mensaje, limit=limit, offset=offset, order=order)
    if not alertas:
        raise HTTPException(status_code=404, detail="No se encontraron alertas con los filtros dados.")
    return alertas

@app.get("/alertas/region/{region}", summary="Alertas por región", tags=["Alertas"])
def get_alertas_por_region(region: str):
    alertas = db.get_alerts_filtered(region=region)
    if not alertas:
        raise HTTPException(status_code=404, detail=f"No se encontraron alertas para la región: {region}")
    return alertas

@app.get("/alertas/tipo/{tipo}", summary="Alertas por tipo", tags=["Alertas"])
def get_alertas_por_tipo(tipo: str):
    alertas = db.get_alerts_filtered(tipo=tipo)
    if not alertas:
        raise HTTPException(status_code=404, detail=f"No se encontraron alertas del tipo: {tipo}")
    return alertas

@app.get("/quien-soy")
def quien_soy():
    instancia = os.getenv("BACKEND_NAME", "Desconocido")
    return {"servidor": instancia}


@app.get("/instancia", summary="Ver instancia del backend", tags=["Diagnóstico"])
def get_instancia_backend():
    return {"instancia": os.getenv("BACKEND_NAME", socket.gethostname())}
