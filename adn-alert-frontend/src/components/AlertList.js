// src/components/AlertList.js
import React from "react";
import moment from "moment";
import { ExclamationTriangleFill } from "react-bootstrap-icons";

export default function AlertList({ alerts, role }) {
  return (
    <div className="mt-4">
      <h4 className="text-danger d-flex align-items-center gap-2">
        <ExclamationTriangleFill />
        Alertas Recibidas ({alerts.length})
      </h4>
      <ul className="list-group">
        {alerts.map((alerta, idx) => {
          const tipo = alerta.tipo || "desconocido";
          const region = alerta.region || "desconocida";
          const mensaje = alerta.mensaje || "Mensaje no disponible";
          const hora = alerta.hora;

          let estilo = "info";
          if (tipo === "sismo") estilo = "danger";
          else if (tipo === "incendio") estilo = "warning";
          else if (tipo === "inundacion") estilo = "primary";

          return (
            <li key={idx} className={`list-group-item list-group-item-${estilo}`}>
              <strong>{tipo.toUpperCase()}</strong> en <em>{region}</em>
              {role === "admin" && hora && (
                <span className="text-muted ms-2">
                  ({moment(hora).format("HH:mm:ss")})
                </span>
              )}
              <br />
              <span>{mensaje}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
