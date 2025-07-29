// src/components/AlertaBanner.js
import React from 'react';
import './AlertaBanner.css';

export default function AlertaBanner({ alerta }) {
  if (!alerta) return null;

  const iconos = {
    sismo: '🌎',
    incendio: '🔥',
    inundacion: '🌊',
  };

  return (
    <div className={`alerta-banner alerta-${alerta.tipo}`}>
      <div className="contenido">
        <span className="icono">{iconos[alerta.tipo] || '🚨'}</span>
        <div className="texto">
          <strong>{alerta.tipo.toUpperCase()}</strong> en <em>{alerta.region}</em>: {alerta.mensaje}
        </div>
      </div>
    </div>
  );
}
