# Design

## Context

Ya existe el recurso `clientes` implementado con las cinco capas (`entities` → `dtos` → `repositories` → `services` → `controllers`) y 19 pruebas en verde. `Base`, `engine` y `get_db` viven en `app/core/database.py`. Todavía no hay specs publicadas en `openspec/specs/`, por lo que `horas` es una capacidad nueva y no modifica ninguna existente. Ver `proposal.md` para la motivación.

## Goals / Non-Goals

**Goals:**

- Registrar, listar, obtener y borrar horas trabajadas respetando las cinco capas.
- Aplicar las reglas de dominio de CU-03: solo clientes de tipo `hora`, minutos enteros positivos y tipo `facturable` o `planificacion`.

**Non-Goals:**

- Calcular montos (CU-06), generar el tarifario PDF (CU-07) ni el dashboard mensual (CU-08). Este cambio solo produce el registro del que después leen esos casos de uso.
- Autenticación o permisos (CU-01).

## Decisions

- **Tabla nueva `horas` con FK hacia `clientes`.** Alternativa considerada: guardar las horas como una columna JSON en el cliente. Se descartó porque obligaría a leer y reescribir el cliente entero en cada registro y dificulta los cálculos por mes de CU-06 y CU-08.
- **La regla "solo clientes de tipo `hora`" vive en el service, no en el controller ni en la entidad.** Es una regla de negocio, no de HTTP ni de esquema: el controller solo traduce HTTP y la entidad solo declara la forma de la tabla. Así el service puede reutilizarse desde el chatbot o un job sin pasar por HTTP.
- **`tipo` como `Enum` `TipoHora` (`facturable` | `planificacion`),** siguiendo el mismo patrón que `TipoCliente`, para que la validación sea del lado del modelo y no una comprobación adicional hecha a mano.
- **`minutos` con `CheckConstraint` mayor a 0 en la tabla** además de la validación del DTO: la restricción queda en la base como última línea de defensa si alguien escribe sin pasar por la API.
- **Borrar un cliente borra sus horas (cascade).** Alternativa considerada: restringir el borrado del cliente. Se eligió cascade porque en el TP el cliente es la unidad de trabajo y no tiene sentido dejar horas huérfanas; queda documentado aquí por si el criterio cambia.
- **El repository nunca lanza `HTTPException`;** solo el service decide 404 o 422. Igual que en `clientes`.

## Risks / Trade-offs

- [Borrar un cliente elimina sus horas] → cascade; documentado arriba. Si se necesita conservar el historial, cambiar a `restrict` y avisar con 409.
- [No hay índice por fecha] → suficiente por ahora; si CU-08 (dashboard mensual) ralentiza, agregar un índice compuesto `(cliente_id, fecha)`.
- [No hay Alembic] → `Base.metadata.create_all` en el `lifespan` crea la tabla nueva al arrancar. Como es SQLite local en el TP, no hay migración pendiente que resolver.

## Open Questions

- ¿CU-06 debe leer las horas al momento o persistir el monto? Se asume lectura al momento, porque el TP dice que el PDF no se guarda.
