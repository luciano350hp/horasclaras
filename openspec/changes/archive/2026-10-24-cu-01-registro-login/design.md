# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-01: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- Contraseñas con PBKDF2-HMAC-SHA256 y sal propia: nunca se guarda ni se devuelve el texto plano.
- Token propio firmado con HMAC (sin librería JWT) para no sumar dependencias.
- **Límite conocido:** el login todavía no protege los demás endpoints ni separa datos por usuario. Queda fuera de alcance.
