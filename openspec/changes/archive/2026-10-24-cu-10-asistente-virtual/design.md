# Design

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Context

CU-10: ver `proposal.md`. Se sigue la arquitectura de 5 capas del proyecto (controller → service → repository → entity, con DTOs).

## Decisions

- Se recuperan los 4 fragmentos más parecidos y se le pasa al modelo solo esa documentación; si no está, debe decir que no sabe.
- Embeddings con fastembed; si no se puede descargar el modelo, plan B local por hash.
- Todo se arma de forma perezosa: sin `GROQ_API_KEY` el servidor arranca igual y el chat responde 503.
- Los tests inyectan un LLM falso: nunca llaman a Groq.
