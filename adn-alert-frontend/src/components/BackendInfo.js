import React, { useEffect, useState } from 'react';
import axios from 'axios';

function BackendInfo() {
  const [instancia, setInstancia] = useState("Cargando...");

  useEffect(() => {
    const obtenerInstancia = async () => {
      try {
        const res = await axios.get('/api/instancia');
        setInstancia(res.data.instancia);
      } catch (error) {
        setInstancia("❌ Error al obtener backend");
      }
    };

    const intervalo = setInterval(obtenerInstancia, 1000);
    return () => clearInterval(intervalo);
  }, []);

  return (
    <div className="alert alert-info text-center">
      <strong>🌀 Respuesta actual desde:</strong><br />
      <span style={{ fontSize: "1.5rem" }}>{instancia}</span>
    </div>
  );
}

export default BackendInfo;
