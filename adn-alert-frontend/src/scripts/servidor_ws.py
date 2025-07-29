import asyncio
import websockets
import json
import random
import time

tipos = ["sismo", "incendio", "inundacion"]
regiones = ["Quito", "Cuenca", "Guayaquil", "Loja", "Ambato"]

async def enviar_alertas(websocket, path):
    while True:
        alerta = {
            "tipo": random.choice(tipos),
            "region": random.choice(regiones),
            "mensaje": "¡Alerta generada automáticamente!"
        }
        await websocket.send(json.dumps(alerta))
        await asyncio.sleep(5)  # cada 5 segundos

start_server = websockets.serve(enviar_alertas, "localhost", 3001)

asyncio.get_event_loop().run_until_complete(start_server)
print("Servidor WebSocket escuchando en ws://localhost:3001")
asyncio.get_event_loop().run_forever()
