# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

Sin clientes no hay a quién registrarle horas ni traducciones. Es la base del dominio: cada cliente cobra por hora o por palabra.

## What Changes

- Entidad `Cliente` con CRUD completo bajo `/api/clientes`.
- Tipos `hora` y `palabra`; tarifa mayor a 0; `descuento_repeticion` de 0 a 100, 50 por defecto.
- Nombre único (409) y máximo 10 clientes (409 el undécimo).
- El nombre se normaliza (sin espacios en los bordes) y no puede quedar vacío (422).

## Capabilities

### New Capabilities

- `clientes`: ver `specs/clientes/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/entities/cliente.py`, `app/dtos/cliente_dto.py`, `app/repositories/cliente_repository.py`, `app/services/cliente_service.py`, `app/controllers/cliente_controller.py`.
- Pruebas: `tests/test_clientes.py (27 tests)`.
