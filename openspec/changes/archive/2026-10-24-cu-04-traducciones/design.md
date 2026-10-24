# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-04: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- Misma estructura que `horas`, para que el cálculo mensual (CU-06) lea ambas igual.
- La regla de tipo de cliente vive en el service; la de repetidas ≤ totales, en el DTO y en un `CheckConstraint`.
- El conteo de palabras lo ingresa la usuaria; no se cuenta el texto automáticamente (post-MVP).
