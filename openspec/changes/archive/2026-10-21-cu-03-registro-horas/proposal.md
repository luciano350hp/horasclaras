# Proposal

## Why

El TP exige registrar las horas que una profesora dicta a cada cliente por hora. Sin ese registro no se puede calcular ningún monto (CU-06) ni emitir el tarifario (CU-07): es la mitad del dominio de cobro por hora y depende de que `clientes` ya exista.

## What Changes

- Nueva entidad `Hora` (registro de horas trabajadas) con su CRUD.
- Regla de dominio: solo se pueden registrar horas a clientes de tipo `hora`; los clientes de tipo `palabra` se rechazan.
- Validaciones: `minutos` entero > 0; `tipo` solo puede ser `facturable` o `planificacion`; `cliente_id` debe existir.
- Nuevos endpoints bajo `/api/horas`.
- Nuevos tests que cubren el caso feliz y los errores 404 y 422.

No se modifica el comportamiento existente de `clientes`: no hay cambios BREAKING.

## Capabilities

### New Capabilities

- `horas`: registro, listado, obtención y borrado de horas trabajadas por clientes de tipo `hora`.

### Modified Capabilities

Ninguna. Todavía no existen specs publicadas en `openspec/specs/`.

## Impact

- Código nuevo: `app/entities/hora.py`, `app/dtos/hora_dto.py`, `app/repositories/hora_repository.py`, `app/services/hora_service.py`, `app/controllers/hora_controller.py`.
- Modificado: `app/main.py` (registrar el router e importar la entidad en el `lifespan`).
- Nuevo archivo de pruebas: `tests/test_horas.py`.
- Sin dependencias nuevas. Sin cambios a la base existente.
