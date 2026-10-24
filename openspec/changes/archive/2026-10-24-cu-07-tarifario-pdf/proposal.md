# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

Las profesionales necesitan un documento prolijo con sus clientes y tarifas para enviar por WhatsApp o mail.

## What Changes

- `GET /api/tarifario/pdf?profesional=...` devuelve un PDF.
- Lista cada cliente con modalidad, tarifa y descuento.

## Capabilities

### New Capabilities

- `tarifario`: ver `specs/tarifario/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/services/tarifario_service.py`, `app/controllers/tarifario_controller.py`.
- Pruebas: `tests/test_tarifario.py (2 tests)`.
