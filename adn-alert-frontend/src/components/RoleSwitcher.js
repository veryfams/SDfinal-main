// src/components/RoleSwitcher.js
import React from 'react';

export default function RoleSwitcher({ role, setRole }) {
  return (
    <div className="btn-group my-3">
      <button className="btn btn-outline-primary" onClick={() => setRole("ciudadano")}>Ciudadano</button>
      <button className="btn btn-outline-danger" onClick={() => setRole("bombero")}>Bombero</button>
      <button className="btn btn-outline-dark" onClick={() => setRole("admin")}>Administrador</button>
    </div>
  );
}
