# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

La usuaria quiere ver de un vistazo cómo le fue en el mes.

## What Changes

- `GET /api/dashboard/{YYYY-MM}`: total facturado, horas facturables y no facturables, palabras, clientes activos y mejor cliente.
- Pantalla de Dashboard con indicadores y barras por cliente.

## Capabilities

### New Capabilities

- `dashboard`: ver `specs/dashboard/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/services/calculo_service.py` (método `dashboard`), `app/controllers/calculo_controller.py`, `frontend/src/pages/Dashboard.jsx`.
- Pruebas: `tests/test_calculos.py (2 tests del dashboard)`.
