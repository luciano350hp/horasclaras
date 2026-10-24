# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

El objetivo del producto es saber cuánto cobrar a cada cliente cada mes, sin cuentas a mano. CU-05 (horas no facturables) se resuelve acá: se registran pero no suman al monto.

## What Changes

- `GET /api/calculos/{YYYY-MM}` con filtro opcional `cliente_id`.
- Monto por hora y por palabra con descuento por repetición.
- Las horas de planificación se informan aparte y nunca se cobran.

## Capabilities

### New Capabilities

- `calculos`: ver `specs/calculos/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/dtos/calculo_dto.py`, `app/services/calculo_service.py`, `app/controllers/calculo_controller.py`.
- Pruebas: `tests/test_calculos.py (7 tests)`.
