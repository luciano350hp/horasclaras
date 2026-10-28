# Proposal

> **Spec primero.** Este cambio se escribió el 2026-10-28 *antes* de implementar el código.

## Why

El PRD (feature "Contador de palabras con presupuesto", prioridad bloqueante) pide que la traductora pegue un texto y la app cuente las palabras, detecte repeticiones exactas y calcule el precio. El CU-04 implementado solo registra trabajos con palabras ingresadas a mano; falta el presupuesto automático.

## What Changes

- Endpoint `POST /api/presupuestos` que recibe `{texto, cliente_id}` y devuelve conteo, repetidas, descuento y monto.
- Solo para clientes de tipo `palabra`.
- No guarda nada: es un presupuesto, no un trabajo registrado.
- Pestaña "Presupuesto" en el frontend.

## Capabilities

### New Capabilities

- `presupuestos`: ver `specs/presupuestos/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/dtos/presupuesto_dto.py`, `app/services/presupuesto_service.py`, `app/controllers/presupuesto_controller.py`, `app/main.py`, `frontend/src/pages/Presupuesto.jsx`, `frontend/src/App.jsx`, `frontend/src/api.js`.
- Pruebas: `tests/test_presupuestos.py`.
