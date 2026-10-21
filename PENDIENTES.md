# HorasClaras — Documento maestro del TP

**Esto es tu mapa.** Un solo lugar con: qué pide el profe, qué tenés hecho, qué falta, qué mostrás en la demo y qué sigue. Nada más.

Fecha entrega final: **27/10/2026**. Demo (no obligatoria): **semana del 20/10**.

---

# PARTE 1 — Qué PIDE el profe (los 5 puntos del TP)

Aprueba con **7 de 10 puntos**.

| # | Punto | Vale | Qué significa |
|---|---|---|---|
| 1 | **Funcionalidad** | hasta 3 | Tener **≥7 de los 10 casos de uso** funcionando |
| 2 | **AI Engineering** | hasta 3 | `AGENTS.md` + skills (`SKILL.md`) + SDD (`openspec/`) |
| 3 | **README** | hasta 1 | Un README completo que explique todo |
| 4 | **MCP** | hasta 1 | Mínimo 2 servidores MCP, al menos 1 externo |
| 5 | **Chatbot LangChain** | hasta 2 | Asistente virtual con LangChain + Groq, integrado en la web |

---

# PARTE 2 — Los 10 Casos de Uso (CU)

| CU | Qué hace | Estado |
|---|---|---|
| CU-01 | Registro e inicio de sesión de usuaria | ❌ falta |
| **CU-02** | **Alta de cliente** (tipo hora/palabra, tarifa, % descuento) | ✅ **HECHO** |
| **CU-03** | **Registro de horas trabajadas por cliente** | ✅ **HECHO** |
| CU-04 | Registro de traducción (palabras totales/repetidas) | ❌ falta |
| CU-05 | Registro de horas no facturables (planificación) | ❌ falta |
| CU-06 | Cálculo automático del monto por cliente/mes | ❌ falta |
| CU-07 | Generación y descarga del tarifario mensual en PDF | ❌ falta |
| CU-08 | Dashboard con resumen mensual | ❌ falta |
| CU-09 | Suscripción a lista de espera (landing pública) | ❌ falta |
| CU-10 | Consulta al asistente virtual (chatbot) | ❌ falta |

**Tenés 2 de 10.** Para el punto 1 necesitás **al menos 7**. Orden sugerido: CU-05 → CU-09 → CU-06 → CU-04 → CU-08.

---

# PARTE 3 — Tu estado de puntaje (real)

| # | Punto | Estado | Puntos |
|---|---|---|---|
| 1 | Funcionalidad | 2/10 CU | ⚠️ ~0.6 / 3 |
| 2 | AI Engineering | ✅ completo | **3 / 3** |
| 3 | README | ✅ completo | **1 / 1** |
| 4 | MCP | ✅ 4 conectados | **1 / 1** |
| 5 | Chatbot | ❌ nada | **0 / 2** |

**Total asegurado: ~5.6 / 10.** Te faltan ~1.4 puntos para aprobar.
**Cómo los sacás:** 2 casos de uso más (subís a 4/10 CU) **o** el chatbot (2 pts).

---

# PARTE 4 — Qué MOSTRAR en la demo

## Demo sin servidor (7 clicks en VS Code, siempre funciona)

En la barra izquierda de VS Code, click en cada uno y decí la frase:

| # | Abrí | Frase para decir |
|---|---|---|
| 1 | `README.md` | "El README: arquitectura, casos de uso y bitácora del entorno de IA." |
| 2 | `AGENTS.md` | "El contexto del agente: las reglas que la IA lee siempre." |
| 3 | `opencode.json` | "Los MCP: filesystem, engram, memory y context7, que es el externo." |
| 4 | `.opencode/skills/` | "Skills: recetas que la IA usa sola cuando hace falta." |
| 5 | `.opencode/agents/revisor.md` | "Un agente revisor: audita el código pero no puede modificarlo." |
| 6 | `openspec/` | "SDD: las especificaciones antes del código." |
| 7 | `app/` | "Arquitectura de 5 capas: controller, service, repository, entity y dto." |

## Demo con servidor (opcional, si querés mostrar la API viva)

**Primero encendé el servidor** en una consola PowerShell:

```powershell
cd C:\Users\Napo\Documents\HorasClaras
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Va a quedar "colgado" mostrando `Application startup complete.` → **eso significa que está funcionando. NO cierres esa consola.**

Después abrí el navegador en:

```
http://127.0.0.1:8000/docs
```

`/docs` es la página web con botones azules para probar la API. **No es un archivo**, existe solo mientras el servidor está encendido.

Para apagarlo: en esa consola apretá `Ctrl + C`.

## Demo de tests (opcional)

En OTRA consola (el servidor sigue prendido en la primera):

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Sale **44 passed**.

## Frase de cierre

> "El stack es React + Vite en el frontend, FastAPI + SQLAlchemy en el backend, SQLite, y para el chatbot LangChain con Groq. El entorno asistido por IA es OpenCode con AGENTS.md, skills, SDD y MCP. Ya tengo 2 casos de uso completos y voy por los siguientes."

---

# PARTE 5 — Qué FALTA para la entrega final (27/10)

Orden de prioridad:

| Prioridad | Qué hacer | Por qué |
|---|---|---|
| 🔴 1 | **MCP de GitHub** | El TP nombra GitHub como MCP externo (tenés context7, que también sirve, pero GitHub es el del enunciado) |
| 🔴 2 | **Chatbot LangChain + Groq** | Vale 2 puntos |
| 🔴 3 | **Casos de uso hasta 7** | Vale hasta 3 puntos (tenés 2) |
| 🔴 4 | **Frontend React + Vite** | El TP lo pide explícito |
| 🟡 5 | CU-07 PDF con ReportLab | 1 caso de uso |

---

# PARTE 6 — Dónde está cada cosa en tu proyecto

```
C:\Users\Napo\Documents\HorasClaras\
│
├── README.md                    ← punto 3 del TP
├── AGENTS.md                    ← punto 2 (contexto del agente)
├── DEMO.md                      ← TU chuleta (NO se muestra, es para vos)
├── PENDIENTES.md                ← este documento
├── opencode.json                ← punto 4 (MCP)
│
├── .opencode\
│   ├── skills\                  ← punto 2 (skills)
│   └── agents\revisor.md        ← punto 2 (agente)
│
├── openspec\                    ← punto 2 (SDD)
│   └── changes\
│       └── cu-03-registro-horas\    ← spec del CU-03
│
├── app\                         ← el código (5 capas)
│   ├── entities\                ← tablas (SQLAlchemy)
│   ├── dtos\                    ← datos que entran/salen (Pydantic)
│   ├── repositories\            ← consultas a la base
│   ├── services\                ← reglas de negocio
│   ├── controllers\             ← endpoints HTTP
│   ├── core\config.py           ← configuración
│   └── main.py                  ← el "servidor" (se enciende con uvicorn)
│
└── tests\                       ← 44 tests que pasan
```

---

# PARTE 7 — Glosario (para no perderte)

| Palabra | Qué es |
|---|---|
| **Servidor** | El programa que se enciende con el comando `uvicorn`. Mientras está prendido, `/docs` funciona. |
| **`/docs`** | Página WEB con los endpoints para probar. No es un archivo. Necesita el servidor prendido. |
| **MCP** | Servidor externo que le da herramientas a la IA. Tenés 4. |
| **Skill** | Receta que la IA carga sola cuando la necesita. |
| **Agente** | Un rol de IA con permisos limitados (ej: el revisor no puede modificar código). |
| **SDD** | Especificar antes de programar. Va en `openspec/`. |
| **CU** | Caso de uso. Son 10. Tenés 2 hechos. |
| **Frontend** | La parte visual (React). Todavía no existe. |
| **Chatbot** | El asistente virtual (CU-10). Todavía no existe. |
| **RAG / base vectorial** | Técnica del chatbot para responder con TUS documentos. |
