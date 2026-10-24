# HorasClaras

Sistema de gestión de horas y tarifas para profesionales freelance (profesoras de idiomas y traductoras).

**TP de IA Engineering (Cohorte 2, UNLa)** — Luciano Napoleone.

El proyecto se desarrolla con **Spec-Driven Development (SDD)** y un entorno de contexto armado para el agente (reglas, skills, agentes y MCP). Las reglas de trabajo del agente están en `AGENTS.md`; las especificaciones de cada caso de uso, en `openspec/`.

> 📘 **Documentación completa en lenguaje simple:** [`docs/DOCUMENTACION.md`](docs/DOCUMENTACION.md)

## Stack

Python 3.14 · FastAPI · SQLAlchemy 2.0 · SQLite · Pydantic v2 · pytest

## Arquitectura

Cinco capas con dependencia en una sola dirección. Cada capa le habla únicamente a la siguiente:

```
controller  ->  service  ->  repository  ->  entity (SQLAlchemy)
     \           |            |
     +-----------+-----------+--> dto (Pydantic, entra y sale por controller/service)
```

| Capa | Responsabilidad | Ejemplo |
|---|---|---|
| `controllers/` | Solo HTTP. Router FastAPI, `response_model`, `Depends(get_db)`. Cero lógica de negocio, cero SQL. | `cliente_controller.py` define `POST /api/clientes/` |
| `services/` | Reglas de negocio y validación. Lanza `HTTPException` (404, 409, 422). Devuelve DTOs, no entidades. | "No más de 10 clientes", "nombre repetido da 409" |
| `repositories/` | CRUD con SQLAlchemy. Recibe `db` como primer argumento. `commit()`/`refresh()` van acá. Nunca lanza `HTTPException`. | `cliente_repository.py` |
| `entities/` | Únicamente el modelo ORM (`Mapped`, `mapped_column`, `CheckConstraint`). Un archivo por entidad. | `cliente.py`: nombre, tipo, tarifa, descuento |
| `dtos/` | Pydantic v2. `XCreate`, `XUpdate`, `XRead` (`from_attributes=True`). Definen qué entra y qué sale. | `ClienteCreate`, `ClienteRead` |
| `core/` | Configuración y conexión a la base. | `config.py`, `database.py` |

**Regla dura:** la entidad no sale de la capa repository. El controller nunca toca `db` directamente. Si hace falta una consulta nueva, va en el repository; si hace falta una regla nueva, va en el service.

```
app/
├── main.py                 # app FastAPI, lifespan, routers
├── core/
│   ├── config.py           # settings desde .env
│   └── database.py         # engine, SessionLocal, Base, get_db
├── entities/               # modelos ORM
├── dtos/                   # schemas Pydantic
├── repositories/           # CRUD SQLAlchemy
├── services/               # reglas de negocio
└── controllers/            # routers HTTP
tests/                      # suite de pytest
openspec/                   # specs (SDD)
```

## Casos de uso

| CU | Descripción | Estado |
|---|---|---|
| CU-01 | Registro / login | **implementado** (back + front) |
| CU-02 | Alta de cliente | **implementado** (back + front) |
| CU-03 | Registro de horas | **implementado** (back + front) |
| CU-04 | Trabajo de traducción (palabras totales / repetidas) | **implementado** (back + front) |
| CU-05 | Horas no facturables | **implementado** (back + front) |
| CU-06 | Cálculo del monto por cliente y mes | **implementado** (back + front) |
| CU-07 | Tarifario PDF | **implementado** (back + front) |
| CU-08 | Dashboard mensual | **implementado** (back + front) |
| CU-09 | Lista de espera | **implementado** (back + front) |
| CU-10 | Asistente virtual (chatbot) | **implementado** (back + front) |

### Reglas de dominio

- Dos tipos de cobro: `hora` (clases) y `palabra` (traducciones).
- Máximo 10 clientes. La tarifa debe ser mayor a 0.
- `descuento_repeticion`: porcentaje 0..100 (por defecto 50) sobre las palabras **repetidas**, no sobre el total.
- Horas: solo para clientes `hora`; minutos enteros > 0; tipo `facturable` o `planificacion` (esta última **nunca se cobra**).
- Monto por hora = (minutos facturables / 60) × tarifa.
- Monto por palabra = (totales − repetidas) × tarifa + repetidas × tarifa × (1 − descuento/100).
- Los cálculos se hacen por cliente y por mes (formato `YYYY-MM`).
- Se usa `Decimal`, nunca `float`. En JSON los decimales viajan como string (`"0.12"`).
- El PDF del tarifario se calcula al momento; no se guarda.

## Arranque

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Docs interactivas de la API en http://127.0.0.1:8000/docs

### Frontend (React + Vite)

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Abrir http://localhost:5173 (el backend tiene que estar corriendo en el puerto 8000). Pantallas: login/registro, dashboard, clientes, horas, traducciones, cobro del mes, tarifario PDF y lista de espera.

## Asistente virtual (CU-10)

RAG con **LangChain + Groq + Chroma** (base vectorial). Los documentos de `knowledge/*.md` se parten en fragmentos, se indexan en Chroma (`data/chroma`, se crea sola en la primera pregunta) y, por cada pregunta, se recuperan los 4 fragmentos más parecidos y se le pasan a Groq como contexto. El historial se guarda en SQLite por `conversation_id`.

Para activarlo hace falta una clave gratis de https://console.groq.com. Se pone en `.env` (nunca se sube):

```
GROQ_API_KEY=tu_clave
GROQ_MODEL=openai/gpt-oss-20b
```

Embeddings: `fastembed` (modelo multilingüe local, se descarga la primera vez). Si no se puede descargar, usa un plan B local por hash (`EMBEDDINGS_BACKEND=hash` fuerza ese modo). Sin `GROQ_API_KEY` el endpoint responde 503 con un mensaje claro. Los tests usan un LLM falso, así que no gastan cuota.

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest
```

La suite monta una base SQLite en memoria (`StaticPool`) y sobreescribe `get_db` vía `app.dependency_overrides`, por lo que **no toca `horasclaras.db`**.

## Configuración

Copiar `.env.example` a `.env` para cambiar la base de datos.

```
DATABASE_URL=sqlite:///./horasclaras.db
```

`DATABASE_URL` se lee de `.env` vía pydantic-settings (`app/core/config.py`). El path de SQLite se resuelve absoluto desde el archivo de config, no desde el cwd. `.env` está en `.gitignore`; `.env.example` es la plantilla.

## API

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |
| GET | `/api/clientes/` | Listar clientes (`skip`, `limit`) |
| POST | `/api/clientes/` | Crear cliente |
| GET | `/api/clientes/{id}` | Obtener cliente |
| PATCH | `/api/clientes/{id}` | Actualizar campos parciales |
| DELETE | `/api/clientes/{id}` | Eliminar cliente |
| GET | `/api/horas/` | Listar horas (filtro opcional `cliente_id`) |
| POST | `/api/horas/` | Registrar una hora |
| GET | `/api/horas/{id}` | Obtener una hora |
| DELETE | `/api/horas/{id}` | Eliminar una hora |
| GET/POST | `/api/traducciones/` | Listar / registrar un trabajo de traducción |
| GET/DELETE | `/api/traducciones/{id}` | Obtener / eliminar |
| GET | `/api/calculos/{YYYY-MM}` | Monto por cliente del mes (`cliente_id` opcional) |
| GET | `/api/dashboard/{YYYY-MM}` | Totales y ranking del mes |
| GET | `/api/tarifario/pdf` | Tarifario en PDF (se genera al vuelo, no se guarda) |
| POST/GET | `/api/waitlist` | Anotarse en la lista de espera (409 si el email ya existe) |
| POST | `/api/auth/registro` · `/api/auth/login` | Crear cuenta / obtener token |
| GET | `/api/auth/me` | Usuario del token |
| POST | `/api/chat` | Preguntarle al asistente (`mensaje`, `conversation_id` opcional) |
| GET | `/api/chat/{conversation_id}` | Historial de una conversación |

```json
{
  "nombre": "Escuela Norte",
  "tipo": "hora",
  "tarifa": "25.00",
  "descuento_repeticion": "5.00"
}
```

`tipo` es `hora` o `palabra`. `tarifa` es el precio por unidad. `descuento_repeticion` es un porcentaje entre 0 y 100 aplicado a las palabras repetidas.

Errores: `404` recurso inexistente, `409` nombre duplicado, `422` datos inválidos (incluye registrar una hora para un cliente que no es de tipo `hora`).

---

# Instalación desde cero (Windows / PowerShell)

```powershell
git clone https://github.com/luciano350hp/horasclaras.git
cd horasclaras
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Si PowerShell no deja activar el venv: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y reintentar.

---

# AI Engineering (bitácora del proceso)

## Esquema de trabajo

Se evaluó el **setup del agente** (cómo se pensó y se armó), más que la calidad del código. El esquema tiene tres piezas obligatorias que se apoyan entre sí: **reglas de contexto (`AGENTS.md`) + skills + SDD**.

```
Plan  ->  specs  ->  Build  ->  pytest  ->  revisor  ->  aprobar / archivar
(propone) (SDD)     (código)   (verifica)  (audita)     (loop si falla)
```

## Herramientas

- **OpenCode** como agente de terminal (modos Plan y Build, se alternan con Tab). Modelos gratuitos del propio OpenCode.
- **OpenSpec** para SDD (Spec-Driven Development), integrado a OpenCode.
- **Git / GitHub** para el control de versiones y la entrega.

## Contexto del agente

- **`AGENTS.md`**: stack con versiones exactas, arquitectura de 5 capas, convenciones de nombres, reglas anti-alucinación y reglas de dominio. Es lo primero que se carga en cada conversación.
- **Skills** (`.opencode/skills/`): se cargan solas según la descripción, cuando el pedido las necesita.
  - `crear-caso-de-uso`: el orden de capas y tests para agregar un CU.
  - `reglas-tarifas`: las fórmulas de cobro por hora y por palabra.
- **Agente `revisor`** (`.opencode/agents/revisor.md`): solo lectura (`permission: {edit: deny, bash: deny}`). Audita acoplamiento, tipos, uso de `Decimal` y cobertura de tests.
- **Agente `backend`** (`.opencode/agents/backend.md`): especializado en el backend (`app/`). Sigue la arquitectura de 5 capas, SQLAlchemy 2.0.x, Pydantic v2 y las reglas de `AGENTS.md`.
- **Agente `frontend`** (`.opencode/agents/frontend.md`): especializado en el frontend **React + Vite**. Consume la API y respeta que las reglas de negocio viven en el backend.
- **`.aisignore`** y **`.gitignore`**: firewall de contexto. Excluyen `.env`, `.venv`, bases `*.db`, `node_modules` y caches, para que nunca se indexen ni se suban.

## MCP configurados (`opencode.json`)

| Servidor | Tipo | Rol en el desarrollo |
|---|---|---|
| `filesystem` | Interno (local, vía `cmd /c npx`) | Leer y escribir **solo dentro** de la carpeta del proyecto (ruta absoluta permitida) |
| `engram` | Interno (local) | Memoria persistente entre sesiones: recuperar decisiones y contexto sin releer el repo |
| `context7` | **Externo** (remoto, `https://mcp.context7.com/mcp`) | Consultar documentación actualizada de FastAPI, SQLAlchemy y Pydantic para no usar APIs obsoletas |

Mínimo exigido: 2 servidores, al menos 1 externo. **Cumplido** (3 servidores en el proyecto, 1 externo).

## Metodología (SDD con OpenSpec)

1. Se define el caso de uso con el CLI de OpenSpec: `openspec new change "<id>"`.
2. Se generan, **antes de programar**, los artifacts del cambio:
   - `proposal.md` — qué se hace y por qué.
   - `specs/<capacidad>/spec.md` — requisitos con escenarios *cuando… entonces…* (`SHALL` / `MUST`).
   - `design.md` — decisiones técnicas y alternativas descartadas.
   - `tasks.md` — pasos con su forma de verificación.
3. Se valida la spec contra su formato: `openspec validate --changes "<id>" --strict`.
4. **Modo Build**: se implementan las 5 capas y se corre `pytest` mostrando la salida real.
5. **`@revisor`** audita el cambio. Si hay problemas, se vuelve a Plan (loop de autocorrección).
6. Se aprueba y se archiva el cambio en `openspec/changes/archive/`.

Las specs se escriben en español, pero los encabezados estructurales y las palabras clave (`SHALL`, `MUST`, `WHEN`, `THEN`) van en inglés, que es el idioma en el que OpenSpec las interpreta.

## Prompts clave

Patrón que se usó para cada caso de uso (prompts cortos, una tarea por vez):

- **Alta de cliente:** *"Implementá CU-02 siguiendo la skill `crear-caso-de-uso`: entidad, DTOs, repository, service, controller y tests. Antes revisá la spec en `openspec/`. Al terminar, corré pytest y pegame la salida real."*
- **Registro de horas:** *"CU-03: solo clientes de tipo `hora`; minutos enteros > 0; tipo `facturable` o `planificacion`. La validación del tipo de cliente va en el service y devuelve 422."*
- **Spec primero:** *"Generá el proposal y la spec de CU-03 con OpenSpec; no escribas código todavía."*
- **Auditoría:** *"@revisor auditá el último cambio."*

Los prompts y las decisiones quedan versionados dentro de cada cambio en `openspec/changes/`.

## Iteraciones y problemas resueltos

- **SQLAlchemy 2.1 bloqueado por Windows Application Control:** un `.pyd` de la 2.1.x no carga (`ImportError: DLL load failed while importing _util_cy`). Se fijó `sqlalchemy>=2.0,<2.1` en `pyproject.toml` y `requirements.txt`. No se "arregla" actualizando.
- **Regla de negocio mal entendida:** el `descuento_repeticion` se aplicaba al total de la factura. Se corrigió a que aplica **solo a las palabras repetidas** (documentado en la skill `reglas-tarifas` y en `AGENTS.md`).
- **`npx` falla con `ENOENT` en Windows:** los MCP locales se lanzan con `["cmd","/c","npx", ...]` en vez de `["npx", ...]`.
- **Rutas de SQLite relativas al cwd:** arrancar uvicorn desde otra carpeta cambiaba la base. Se ancló el path absoluto al directorio del archivo de config.
- **Consumo de tokens:** prompts en inglés, una sesión nueva por caso de uso y compactación al pasar el 70 % de la ventana de contexto.
- **Loop de autocorrección:** en CU-03 la primera propuesta validaba el tipo de cliente en el controller; el revisor marcó que era una regla de negocio y se movió al service.

## Estructura de las instrucciones

| Archivo | Cuándo se carga | Para qué |
|---|---|---|
| `AGENTS.md` | Siempre, automático | Reglas generales, stack y arquitectura |
| `.opencode/skills/*/SKILL.md` | Solo cuando el pedido coincide con su descripción | Un procedimiento detallado (crear un CU, calcular tarifas) |
| `.opencode/agents/revisor.md` | Cuando se invoca | Un rol con permisos propios (solo lectura) |
| `opencode.json` | Al iniciar la sesión | Conexión a los servidores MCP |

## Qué quedó en el repo para evaluar el setup

```
AGENTS.md                     reglas del agente
opencode.json                 configuración de los MCP
.aisignore / .gitignore       firewall de contexto
.opencode/skills/             skills (crear-caso-de-uso, reglas-tarifas)
.opencode/agents/revisor.md   agente auditor de solo lectura
.opencode/commands/opsx-*     comandos de OpenSpec para OpenCode
openspec/                     specs, cambios y archivo (SDD)
```
