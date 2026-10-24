# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

Captar emails de personas interesadas antes del lanzamiento.

## What Changes

- `POST /api/waitlist` y `GET /api/waitlist`.
- Email normalizado a minúsculas, con formato válido y único.

## Capabilities

### New Capabilities

- `waitlist`: ver `specs/waitlist/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/entities/suscripcion.py`, `app/dtos/suscripcion_dto.py`, `app/repositories/suscripcion_repository.py`, `app/services/suscripcion_service.py`, `app/controllers/suscripcion_controller.py`.
- Pruebas: `tests/test_waitlist.py (4 tests)`.
