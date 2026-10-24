# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-02: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- El límite de 10 clientes y la unicidad del nombre viven en el service; la unicidad también se defiende con `unique` en la base (carrera entre pedidos).
- `descuento_repeticion` por defecto 50: es el estándar de la industria de traducción.
- Dinero con `Decimal` / `Numeric(10,2)`, nunca `float`.
