# AGENTS.md (Backend)

Este archivo aplica **únicamente** al código dentro de `app/`. Para reglas globales del proyecto, ver `../AGENTS.md`.

## Alcance
- Trabajar solo en `app/` (controllers, services, repositories, entities, dtos, core, main.py)
- Tests en `tests/`
- NO tocar frontend, `.opencode/`, `openspec/` ni configuración MCP sin pedido explícito

## Arquitectura obligatoria: 5 capas
```
controller -> service -> repository -> entity (SQLAlchemy)
     \           |            |
     +-----------+-----------+--> dto (Pydantic v2)
```

- **controllers/**: Solo HTTP. `APIRouter`, `response_model`, `Depends(get_db)`. Sin lógica de negocio ni SQL.
- **services/**: Reglas de negocio. Única capa que lanza `HTTPException` (404, 409, 422). Devuelve DTOs, nunca entidades.
- **repositories/**: CRUD/consultas. Recibe `db: Session` primero. `commit()/refresh()` van acá. **Nunca** lanza `HTTPException`.
- **entities/**: Solo ORM. `Mapped[...]`, `mapped_column`, `CheckConstraint`. **La entidad NO sale del repository**.
- **dtos/**: Pydantic v2. `XCreate`, `XUpdate`, `XRead` con `model_config = ConfigDict(from_attributes=True)`.

## Convenciones
- Dominio en español (`Cliente`, `Hora`). Librerías en inglés.
- Archivos `snake_case` singular: `cliente_service.py`
- Un router por recurso. Registrar en `app/main.py` con `include_router`. Importar entidades en `lifespan` para crear tablas.
- **Decimal siempre**. Nunca `float`. JSON viaja como string.
- `tarifa > 0`. `descuento_repeticion` 0..100, **default 50**. Máximo **10 clientes**.
- Horas solo para clientes `hora`. Minutos > 0. `facturable` o `planificacion` (nunca se cobra).
- `__init__.py` están vacíos a propósito (paquete Python).
- `__pycache__/` generado automáticamente, ignorado por git.

## Flujo
1. Usar OpenSpec si es caso nuevo (`openspec/changes/<id>/`)
2. Seguir las 5 capas
3. Agregar tests en `tests/test_<recurso>.py`
4. Verificar con `.\.venv\Scripts\python.exe -m pytest` (salida real)
5. No commitear sin pedido
