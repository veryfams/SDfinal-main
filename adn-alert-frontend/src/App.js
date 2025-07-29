import React, { useState, useEffect } from 'react';
import RoleSwitcher from './components/RoleSwitcher';
import CiudadanoView from './views/CiudadanoView';
import BomberoView from './views/BomberoView';
import AdminView from './views/AdminView';
import AlertList from './components/AlertList';
import { connectWebSocket, closeWebSocket } from './services/websocket';
import AlertaBanner from './components/AlertaBanner';
import Header from './components/Header';
//import BackendInfo from './components/BackendInfo'; // 👈 Agrega esto


function App() {
  const [role, setRole] = useState("ciudadano");
  const [alerts, setAlerts] = useState([]);
  const [ultimaAlerta, setUltimaAlerta] = useState(null);

  useEffect(() => {
    console.log("🚀 Montando App.js");
    connectWebSocket((data) => {
      console.log("📥 Alerta recibida en App.js:", data);
      const alertaConHora = { ...data, hora: new Date().toISOString() };
      setAlerts((prev) => [...prev, alertaConHora]);
      setUltimaAlerta(alertaConHora);

      // 🔊 Sonido de alerta
      const audio = new Audio("/alerta.mp3");
      audio.play().catch((err) => console.warn("⚠️ No se pudo reproducir el sonido:", err));
    });

    return () => closeWebSocket();
  }, []);

  const alertasFiltradas = alerts.filter((a) => {
    if (role === "ciudadano") return true;
    if (role === "bombero") return a.tipo === "incendio" || a.tipo === "inundacion";
    return true;
  });

  return (
    <div className="container py-4">
      {/* ✅ Banner con última alerta */}
      <AlertaBanner alerta={ultimaAlerta} />

      {/* ✅ Encabezado moderno */}
      <Header />

      {/* ✅ Selector de rol */}
      <div className="d-flex justify-content-center mb-3">
        <RoleSwitcher role={role} setRole={setRole} />
      </div>

      {/* ✅ Vista específica según rol */}
      {role === "ciudadano" && <CiudadanoView />}
      {role === "bombero" && <BomberoView />}
      {role === "admin" && <AdminView />}

      {/* ✅ Lista filtrada de alertas */}
      <AlertList alerts={alertasFiltradas} role={role} />
    </div>
  );
}

export default App;
