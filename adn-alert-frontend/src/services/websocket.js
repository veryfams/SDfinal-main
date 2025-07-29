// src/services/websocket.js
let socket;
let reconnectTimeout;

/**
 * Conecta al WebSocket backend y maneja los mensajes recibidos.
 * @param {Function} onMessage - Función callback para manejar los mensajes entrantes.
 */
export const connectWebSocket = (onMessage) => {
  const wsUrl = `ws://${window.location.hostname}:8000/ws`;
  socket = new WebSocket(wsUrl);

  socket.onopen = () => {
    console.log("✅ WebSocket conectado con:", wsUrl);
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      console.log("📥 Alerta recibida por WebSocket:", data);
      if (onMessage) onMessage(data);
    } catch (err) {
      console.warn("⚠️ No se pudo parsear el mensaje:", event.data);
    }
  };

  socket.onerror = (error) => {
    console.error("❌ Error en WebSocket:", error);
  };

  socket.onclose = (event) => {
    console.warn(`🔌 WebSocket cerrado [Código: ${event.code}]. Reintentando en 5s...`);
    reconnectTimeout = setTimeout(() => connectWebSocket(onMessage), 5000);
  };
};

/**
 * Cierra manualmente la conexión WebSocket si está abierta.
 */
export const closeWebSocket = () => {
  if (reconnectTimeout) clearTimeout(reconnectTimeout);
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.close();
    console.log("🔒 WebSocket cerrado manualmente.");
  }
};
