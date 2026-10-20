---
name: crear-caso-de-uso
description: Use when implementing a new use case or endpoint in HorasClaras (entity, dto, repository, service, controller and tests).
---

# Crear un caso de uso en HorasClaras

Seguir siempre este orden y respetar las 5 capas descriptas en AGENTS.md.

1. Leer la spec del caso de uso en `openspec/changes/<cambio>/specs/` antes de escribir codigo.
2. `app/entities/<recurso>.py`: solo el modelo ORM, con CheckConstraint si el dominio lo exige.
3. `app/dtos/<recurso>_dto.py`: `XCreate`, `XUpdate`, `XRead` (Pydantic v2, `from_attributes=True`).
4. `app/repositories/<recurso>_repository.py`: CRUD y consultas. Nunca lanza HTTPException.
5. `app/services/<recurso>_service.py`: reglas de negocio. Lanza HTTPException (404, 409, 422). Devuelve DTOs.
6. `app/controllers/<recurso>_controller.py`: solo HTTP, `prefix="/api/<recurso>"`, `Depends(get_db)`.
7. Registrar el router en `app/main.py` e importar la entidad en el `lifespan`.
8. Tests en `tests/test_<recurso>.py`: happy path y reglas (404, 409, 422).
9. Correr `.\.venv\Scripts\python.exe -m pytest` y mostrar la salida real. No afirmar que funciona sin ejecutarlo.