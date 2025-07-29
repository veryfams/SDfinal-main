import paho.mqtt.client as mqtt
import datetime

class MQTTClient:
    def __init__(self, broker_host, broker_port, topic, db):
        self.client = mqtt.Client()
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.db = db
        self.on_message_callback = None

    def on_connect(self, client, userdata, flags, rc):
        print(f"✅ Conectado a MQTT Broker con código {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        timestamp = datetime.datetime.utcnow()
        print(f"[MQTT] 📥 {msg.topic}: {payload}")
        self.db.insert_alert(msg.topic, payload, timestamp)
        if self.on_message_callback:
            print("🧪 Ejecutando callback manejar_mensaje...")
            self.on_message_callback(msg.topic, payload, timestamp)

    def start(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_host, self.broker_port, 60)
        self.client.loop_start()

    def set_on_message_callback(self, callback):
        self.on_message_callback = callback
