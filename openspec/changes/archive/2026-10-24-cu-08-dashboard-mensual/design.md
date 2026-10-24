# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-08: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- El dashboard reutiliza el cálculo mensual: una sola fuente de verdad para los montos.
- El frontend no recalcula plata: muestra lo que devuelve la API.
