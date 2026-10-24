# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-05 y CU-06: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- Todo el cálculo vive en un solo service, con `Decimal` y redondeo a centavos (ROUND_HALF_UP).
- Fórmula por hora: minutos facturables / 60 × tarifa. Por palabra: (totales − repetidas) × tarifa + repetidas × tarifa × (1 − descuento/100).
- El mes se valida con formato `YYYY-MM` (422 si no).
