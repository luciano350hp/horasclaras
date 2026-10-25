# Guion para video (10-15 minutos) + PDF de entrega

> Estado: 10 de 10 casos de uso con backend y frontend, 76 tests en verde. Documentación completa en `docs/DOCUMENTACION.md`.

## VIDEO (10-15 min) — YouTube (sin listar) o Google Drive

### 1) Intro (1 min)
- Nombre, apellido, proyecto "HorasClaras".
- Qué es: sistema para profesoras de inglés y traductoras para registrar horas y traducciones, y calcular cuánto cobrar por cliente y por mes.
- Objetivo del video: mostrar el entorno de trabajo con IA y la aplicación funcionando.

### 2) Entorno de IA — lo que más se evalúa (4-5 min)
Mostrar en VS Code, de arriba hacia abajo:
- `AGENTS.md` en jerarquía: general (`AGENTS.md`), backend (`app/AGENTS.md`), frontend (`frontend/AGENTS.md`).
- `.opencode/agents/`: `backend`, `frontend`, `revisor` (este último solo lee: `edit: deny`, `bash: deny`).
- `.opencode/skills/`: las propias (`crear-caso-de-uso`, `reglas-tarifas`) y las de OpenSpec.
- `opencode.json`: 3 MCP (`filesystem`, `context7` externo, `engram`). Contar que se sacó Gentle AI porque pesaba 125 KB y consumía el cupo.
- `openspec/`: `changes/archive/` y `specs/`. Aclarar con honestidad: CU-03 se hizo con spec primero; el resto tiene especificación retroactiva (marcada `retroactive: true`).

### 3) Un caso de uso nuevo con OpenCode + OpenSpec, en vivo (3 min) — RECOMENDADO
Mostrar el flujo real: proponer → especificar → implementar → archivar, con OpenCode. Usar un caso chico. Si OpenCode no responde, decirlo y mostrar el flujo con la spec de CU-03.

### 4) La aplicación funcionando (3 min)
Servidor (terminal 1): `.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload`
Pantallas (terminal 2): `cd frontend` y `npm run dev` → http://localhost:5173
- Registrarse e ingresar (CU-01).
- Crear un cliente por hora y uno por palabra (CU-02).
- Cargar horas facturables y de planificación (CU-03, CU-05).
- Cargar una traducción con palabras repetidas (CU-04).
- "Cobro del mes" y "Dashboard": explicar que la planificación no se cobra y el descuento solo afecta a las repetidas (CU-06, CU-08).
- Descargar el tarifario PDF (CU-07).
- Anotar un email en la lista de espera; repetirlo y mostrar el aviso de duplicado (CU-09).
- Preguntarle al asistente "¿cuántos clientes puedo tener?" (CU-10). Requiere `GROQ_API_KEY` en `.env`.
- Mostrar la regla del cliente número 11 en http://127.0.0.1:8000/docs (409).

### 5) Tests y cierre (1-2 min)
`.\.venv\Scripts\python.exe -m pytest` → **76 passed**.
Mostrar GitHub: https://github.com/luciano350hp/horasclaras
Decir con claridad qué se hizo con qué herramienta (ver `docs/DOCUMENTACION.md`, sección 9) y qué falta: el login todavía no separa los datos por usuario.

Duración total: 12-15 minutos.

## PDF DE ENTREGA

Portada
- Título: Trabajo Práctico Integrador — HorasClaras
- Materia: Arquitectura de Agentes y AI-Augmented Software Engineering — Cohorte 2
- Integrante: Napoleone, Luciano
- Usuario GitHub: luciano350hp
- Repo: https://github.com/luciano350hp/horasclaras
- Video: [pegar el link de YouTube o Drive]

Contenido:
1. Los 10 casos de uso, todos implementados con backend y frontend:

| CU | Nombre |
|---|---|
| CU-01 | Registro / login |
| CU-02 | Alta de cliente |
| CU-03 | Registro de horas |
| CU-04 | Trabajo de traducción (palabras totales y repetidas) |
| CU-05 | Horas no facturables |
| CU-06 | Cálculo del monto por cliente y mes |
| CU-07 | Tarifario PDF |
| CU-08 | Dashboard mensual |
| CU-09 | Lista de espera |
| CU-10 | Asistente virtual (LangChain + Groq + Chroma) |

2. Stack: FastAPI + SQLAlchemy + SQLite; React + Vite; LangChain + Groq + Chroma; OpenCode, AGENTS.md, skills, agentes, OpenSpec, MCP.
3. Esquema de trabajo con IA: jerarquía de AGENTS.md, skills, agentes, SDD, MCP (explicar qué se hizo con OpenCode y qué con otra herramienta).
4. Estado: 76 tests, documentación completa en `docs/DOCUMENTACION.md`, límites conocidos.
