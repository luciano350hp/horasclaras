# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

Las traductoras cobran por palabra y necesitan registrar cuántas palabras tuvo cada trabajo y cuántas eran repetidas.

## What Changes

- Entidad `Traduccion` con CRUD bajo `/api/traducciones`.
- Solo para clientes de tipo `palabra`.
- Las palabras repetidas no pueden superar a las totales.

## Capabilities

### New Capabilities

- `traducciones`: ver `specs/traducciones/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/entities/traduccion.py`, `app/dtos/traduccion_dto.py`, `app/repositories/traduccion_repository.py`, `app/services/traduccion_service.py`, `app/controllers/traduccion_controller.py`.
- Pruebas: `tests/test_traducciones.py (5 tests)`.
