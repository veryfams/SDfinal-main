import asyncio
import json
import logging
import time
from datetime import datetime
import paho.mqtt.client as mqtt
from typing import Dict, List, Callable
import threading

class MQTTAmbassador:
    """
    Ambassador Pattern para MQTT - Proxy inteligente que maneja:
    - Reconexión automática
    - Rate limiting
    - Logging estructurado
    - Métricas de performance
    - Circuit breaker
    """
    
    def __init__(self, broker_host: str, broker_port: int, client_id: str):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id
        self.client = mqtt.Client(client_id)
        
        # Métricas y estado
        self.metrics = {
            'messages_sent': 0,
            'messages_received': 0,
            'connection_attempts': 0,
            'successful_connections': 0,
            'last_activity': None
        }
        
        # Circuit breaker
        self.circuit_state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
        self.failure_count = 0
        self.failure_threshold = 5
        self.timeout_duration = 30
        self.last_failure_time = None
        
        # Rate limiting
        self.rate_limit = 10  # mensajes por segundo
        self.message_timestamps = []
        
        # Callbacks
        self.message_callbacks: Dict[str, List[Callable]] = {}
        
        # Logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f'MQTTAmbassador-{client_id}')
        
        # Setup MQTT client
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_publish = self._on_publish
        
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.metrics['successful_connections'] += 1
            self.circuit_state = 'CLOSED'
            self.failure_count = 0
            self.logger.info(f"✅ Ambassador conectado a MQTT Broker (RC: {rc})")
            
            # Log estructurado para Fluentd
            self._log_structured('mqtt_connection', {
                'status': 'connected',
                'broker': f"{self.broker_host}:{self.broker_port}",
                'client_id': self.client_id,
                'return_code': rc
            })
        else:
            self.failure_count += 1
            self.last_failure_time = time.time()
            self.logger.error(f"❌ Error conectando a MQTT (RC: {rc})")
            
    def _on_disconnect(self, client, userdata, rc):
        self.logger.warning(f"🔌 Ambassador desconectado de MQTT (RC: {rc})")
        self._log_structured('mqtt_disconnection', {
            'status': 'disconnected',
            'return_code': rc,
            'client_id': self.client_id
        })
        
    def _on_message(self, client, userdata, msg):
        # Rate limiting check
        if not self._check_rate_limit():
            self.logger.warning("⚠️ Rate limit excedido, descartando mensaje")
            return
            
        self.metrics['messages_received'] += 1
        self.metrics['last_activity'] = datetime.now().isoformat()
        
        topic = msg.topic
        payload = msg.payload.decode()
        
        # Log estructurado
        self._log_structured('mqtt_message_received', {
            'topic': topic,
            'payload_size': len(payload),
            'qos': msg.qos,
            'retain': msg.retain
        })
        
        # Ejecutar callbacks registrados
        if topic in self.message_callbacks:
            for callback in self.message_callbacks[topic]:
                try:
                    callback(topic, payload, datetime.now())
                except Exception as e:
                    self.logger.error(f"❌ Error en callback: {e}")
                    
    def _on_publish(self, client, userdata, mid):
        self.metrics['messages_sent'] += 1
        self.metrics['last_activity'] = datetime.now().isoformat()
        
    def _check_rate_limit(self) -> bool:
        now = time.time()
        # Limpiar timestamps antiguos (más de 1 segundo)
        self.message_timestamps = [ts for ts in self.message_timestamps if now - ts < 1]
        
        if len(self.message_timestamps) >= self.rate_limit:
            return False
            
        self.message_timestamps.append(now)
        return True
        
    def _check_circuit_breaker(self) -> bool:
        if self.circuit_state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout_duration:
                self.circuit_state = 'HALF_OPEN'
                self.logger.info("🔄 Circuit breaker en HALF_OPEN")
                return True
            return False
        return True
        
    def _log_structured(self, event_type: str, data: dict):
        """Envía logs estructurados que Fluentd puede procesar"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'service': 'mqtt_ambassador',
            'client_id': self.client_id,
            'event_type': event_type,
            'data': data,
            'metrics': self.metrics.copy()
        }
        
        # Escribir a archivo que Fluentd puede leer
        with open('/var/log/mqtt/ambassador.log', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
    def connect(self):
        """Conecta con circuit breaker"""
        if not self._check_circuit_breaker():
            self.logger.warning("⛔ Circuit breaker OPEN - no intentando conexión")
            return False
            
        self.metrics['connection_attempts'] += 1
        
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.circuit_state = 'OPEN'
                self.logger.error("⛔ Circuit breaker OPEN debido a fallos consecutivos")
                
            self.logger.error(f"❌ Error conectando: {e}")
            return False
            
    def subscribe(self, topic: str, callback: Callable):
        """Suscribe a un topic con callback"""
        if topic not in self.message_callbacks:
            self.message_callbacks[topic] = []
        self.message_callbacks[topic].append(callback)
        
        self.client.subscribe(topic)
        self.logger.info(f"📬 Suscrito a topic: {topic}")
        
    def publish(self, topic: str, payload: str, qos: int = 0):
        """Publica mensaje con rate limiting y circuit breaker"""
        if not self._check_circuit_breaker():
            self.logger.warning("⛔ Circuit breaker OPEN - no enviando mensaje")
            return False
            
        if not self._check_rate_limit():
            self.logger.warning("⚠️ Rate limit excedido - no enviando mensaje")
            return False
            
        try:
            result = self.client.publish(topic, payload, qos)
            self._log_structured('mqtt_message_sent', {
                'topic': topic,
                'payload_size': len(payload),
                'qos': qos,
                'message_id': result.mid
            })
            return True
        except Exception as e:
            self.logger.error(f"❌ Error enviando mensaje: {e}")
            return False
            
    def get_metrics(self) -> dict:
        """Retorna métricas del ambassador"""
        return {
            **self.metrics,
            'circuit_state': self.circuit_state,
            'failure_count': self.failure_count,
            'active_subscriptions': len(self.message_callbacks)
        }
        
    def disconnect(self):
        """Desconecta limpiamente"""
        self.client.loop_stop()
        self.client.disconnect()
        self.logger.info("🔒 Ambassador desconectado")
