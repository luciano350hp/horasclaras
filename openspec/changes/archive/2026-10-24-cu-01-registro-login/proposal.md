# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

Las profesionales necesitan una cuenta propia para ingresar a la aplicación.

## What Changes

- Entidad `Usuario` (email único, contraseña cifrada).
- `POST /api/auth/registro`, `POST /api/auth/login` y `GET /api/auth/me`.
- Token firmado con `SECRET_KEY` y vencimiento.

## Capabilities

### New Capabilities

- `auth`: ver `specs/auth/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/entities/usuario.py`, `app/dtos/auth_dto.py`, `app/repositories/usuario_repository.py`, `app/services/auth_service.py`, `app/controllers/auth_controller.py`.
- Pruebas: `tests/test_auth.py (6 tests)`.
