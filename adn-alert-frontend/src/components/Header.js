// src/components/Header.js
import React from 'react';
import { Globe } from 'react-bootstrap-icons';

export default function Header() {
  return (
    <header className="d-flex align-items-center justify-content-between mb-4 border-bottom pb-2">
      <h1 className="text-primary d-flex align-items-center gap-2">
        <Globe size={36} />
        Sistema de Alerta de Desastres
      </h1>
    </header>
  );
}
