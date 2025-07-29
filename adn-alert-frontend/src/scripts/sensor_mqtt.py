import time
import json
import random
import paho.mqtt.client as mqtt

tipos = ["sismo", "incendio", "inundacion"]
regiones = ["Quito", "Cuenca", "Guayaquil", "Loja", "Ambato"]

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    alerta = {
        "tipo": random.choice(tipos),
        "region": random.choice(regiones),
        "mensaje": "¡Simulación automática de alerta!"
    }
    client.publish("alertas/general", json.dumps(alerta))
    print("📤 Alerta enviada:", alerta)
    time.sleep(5)
