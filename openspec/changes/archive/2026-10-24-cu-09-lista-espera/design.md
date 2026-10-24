# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-09: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- Validación de email con expresión regular propia, sin sumar `email-validator`.
- Duplicados detectados tras normalizar a minúsculas.
