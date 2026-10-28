# Estado del proyecto y pendientes

> Actualizado el 27/10/2026. Para entender el proyecto completo: `docs/DOCUMENTACION.md`.

## Casos de uso: 10 de 10 + CU-11 (backend + frontend)

CU-11 Presupuesto de traducción (agregado el 28/10 con la spec escrita antes del código: `openspec/changes/2026-10-28-cu-11-presupuesto/`).

| CU | Estado | Especificación OpenSpec |
|---|---|---|
| CU-01 Registro / login | ✅ | retroactiva |
| CU-02 Alta de cliente | ✅ | retroactiva |
| CU-03 Registro de horas | ✅ | **original** (spec antes del código) |
| CU-04 Trabajo de traducción | ✅ | retroactiva |
| CU-05 Horas no facturables | ✅ | retroactiva (incluida en cálculos) |
| CU-06 Cálculo del monto | ✅ | retroactiva |
| CU-07 Tarifario PDF | ✅ | retroactiva |
| CU-08 Dashboard mensual | ✅ | retroactiva |
| CU-09 Lista de espera | ✅ | retroactiva |
| CU-10 Asistente virtual | ✅ (probado con clave real de Groq: funciona) | retroactiva |

76 tests en verde.

## Puntaje del TP

| # | Qué se evalúa | Puntos | Estado |
|---|---|---|---|
| 1 | Funcionalidad: ≥7 de 10 CU con front y back | 3 | 10/10 hechos |
| 2 | Esquema de trabajo y AI Engineering | 3 | Armado; falta mostrarlo en el video |
| 3 | README | 1 | Actualizado |
| 4 | MCP (mín. 2, al menos 1 externo) | 1 | `filesystem`, `context7` (externo), `engram` |
| 5 | Chatbot LangChain en la web | 2 | Implementado |

## Pendientes

1. ~~**Probar todo en la PC del autor**~~ ✅ hecho (pytest 76/76, servidor, pantallas, asistente con clave real de Groq).
2. ~~**Pasar la rama `cu-completos` a `main`**~~ ✅ `main` ya tiene todo (la única diferencia con `cu-completos` es el `.gitignore`).
3. **Hacer un caso de uso nuevo con OpenCode + OpenSpec en vivo** (spec primero) para mostrar SDD real en el video. Depende de que OpenCode vuelva a funcionar (ver el problema del cupo gratis; alternativa: clave propia de Groq).
4. **Grabar el video** (10–15 min) con `GUIA_VIDEO_PDF.md`.
5. **Armar el PDF de entrega** con los 10 CU, nombre, link del repo y link del video.
6. Confirmar la fecha de entrega con el profesor.
7. Agregar el bloque `github` al MCP (con token en variable de entorno) si se quiere un segundo MCP externo.

## Límites conocidos (decirlos en el video)

- El login no separa los datos por usuario.
- CORS abierto (`*`), para desarrollo.
- SQLite de un solo archivo.
- Las especificaciones de 8 de los 9 cambios archivados son retroactivas.
