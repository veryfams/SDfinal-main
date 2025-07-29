#  Backend - Integración de Base de Datos

Este archivo explica lo que ya está implementado y lo que tú (compañero) debes completar para integrar la base de datos en el backend del sistema de alerta distribuido.

---

##  Lo que YA está funcionando

- El backend (FastAPI) se conecta a un broker MQTT.
- Recibe alertas simuladas desde un script (`sensor_mqtt.py`).
- Reenvía esas alertas en tiempo real a los clientes conectados por WebSocket.
- Está dockerizado y funcionando dentro de `docker-compose`.

---

##  Tu misión: integrar una base de datos

Puedes usar **MongoDB** o **PostgreSQL** (tú eliges). El objetivo es:

1. Guardar cada alerta recibida en la base de datos.
2. Crear una ruta REST para consultar las alertas guardadas.

---

##  Estructura recomendada

Archivos clave:
adn-alert-backend/
├── main.py # FastAPI y WebSocket
├── mqtt_client.py # recibe mensajes MQTT
├── websocket_manager.py # gestiona conexiones WS
├── db.py # aquí creas la conexión a Mongo o Postgres
├── models.py # esquema de alerta (si usas Pydantic)
├── requirements.txt # aquí agregas pymongo o sqlalchemy
├── Dockerfile



---

##  Qué debes hacer

###  1. Conexión a BD (en `db.py`)

- Si usas MongoDB → `pymongo`
- Si usas PostgreSQL → `sqlalchemy` + `asyncpg`

###  2. Guardar alertas (en `mqtt_client.py`)

Dentro de `on_message(...)`, además de reenviar por WebSocket, guarda la alerta en la base de datos.

### 3. Crear ruta REST (en `main.py`)

Ejemplo simple:
```python
@app.get("/alertas")
def listar_alertas():
    return db.obtener_alertas()
