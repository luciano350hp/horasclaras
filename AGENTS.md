# AGENTS.md

HorasClaras: gestión de horas y tarifas para profesionales freelance (profesoras de idiomas y traductoras).

## Jerarquía de AGENTS.md

Este archivo es el general. Para trabajar en una parte, leer además el específico: `app/AGENTS.md` (backend) o `frontend/AGENTS.md` (frontend). Los agentes `backend` y `frontend` de `.opencode/agents/` los siguen.

## Comandos

Siempre con el venv local: `.\.venv\Scripts\python.exe` (o activarlo primero). Sin venv no están las dependencias.

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload   # servidor, docs en /docs
.\.venv\Scripts\python.exe -m pytest                          # tests
.\.venv\Scripts\python.exe -m pytest tests/test_clientes.py    # un archivo
.\.venv\Scripts\python.exe -m pytest tests/test_clientes.py::test_crear_cliente -k  # un test
```

No hay linter, formatter ni typechecker configurado. No los asumas ni los agregues sin pedirlo.

## Restricción de versión: SQLAlchemy 2.0.x

`sqlalchemy>=2.0,<2.1` está pineado a propósito. La 2.1.x incluye un `.pyd` (`sqlalchemy/engine/_util_cy.cp314-win_amd64.pyd`) que Windows bloquea por Control de Aplicaciones en esta máquina: `ImportError: DLL load failed while importing _util_cy`. No "arregles" esto actualizando a 2.1.x.

## Arquitectura: 5 capas, dependencia en una sola dirección

```
controller  ->  service  ->  repository  ->  entity (SQLAlchemy)
     \           |            |
     +-----------+-----------+--> dto (Pydantic, entra y sale por controller/service)
```

- **controller** (`app/controllers/`): solo HTTP. Router FastAPI, `prefix="/api/<recurso>"`, `response_model`, `Depends(get_db)`. Cero lógica de negocio, cero SQL.
- **service** (`app/services/`): reglas de negocio y validación. Lanza `HTTPException` (404 no existe, 409 duplicado). Devuelve DTOs, no entidades.
- **repository** (`app/repositories/`): CRUD con SQLAlchemy. Recibe `db: Session` como primer argumento. `commit()`/`refresh()` van acá. Nunca lanza HTTPException.
- **entity** (`app/entities/`): únicamente el modelo ORM, `Mapped[...]` / `mapped_column`, más `CheckConstraint` de rango cuando el dominio lo exija. Un archivo por entidad.
- **dto** (`app/dtos/`): Pydantic v2. `XCreate`, `XUpdate`, `XRead` (`from_attributes=True`).

Regla dura: **la entidad no sale de la capa repository**. El controller nunca toca `db` directamente. Si necesitás una consulta nueva, va en el repository; si necesitás una regla nueva, va en el service.

## Convenciones

- Dominio y código en español: `Cliente`, `ClienteService`, `ClienteRepository`, `ClienteCreate`. Siglas y nombres de librería en inglés.
- Archivos en `snake_case` y en singular: `cliente.py`, `cliente_service.py`. Carpetas en plural.
- Un router por recurso, instanciado como `service = XService()` a nivel de módulo.
- Montar routers en `app/main.py` con `include_router`; nada más se importa desde controllers hacia arriba.
- Las tablas se crean en el `lifespan` de `app/main.py`. Para registrar una entidad nueva hay que importarla ahí o las tablas no se crean (por eso está el `from app.entities import ... as _noqa`).
- Decimales: `Decimal` en entity, DTO y response. En JSON viajan como string (`"0.12"`), no float. No los compares con `==` contra floats.
- `tarifa` es `gt=0`; `descuento_repeticion` es un porcentaje `0..100` (CHECK constraints en la tabla, no solo validación Pydantic).

## Configuración

- `DATABASE_URL` se lee de `.env` vía pydantic-settings (`app/core/config.py`). `.env` está en `.gitignore`; `.env.example` es la plantilla.
- Default: `sqlite:///<BASE_DIR>/horasclaras.db`. El path se resuelve absoluto desde el archivo de config, no desde el cwd: arrancar uvicorn desde otro directorio no cambia la base.
- Para SQLite el engine usa `check_same_thread=False` (FastAPI corre el handler en un threadpool). `connect_args` solo se aplica si la URL es SQLite, así una futura Postgres no rompe.
- `extra="ignore"` en la config: variables de entorno desconocidas no rompen el arranque.

## Tests

- `tests/conftest.py` monta una DB en memoria con `StaticPool` y sobreescribe `get_db` vía `app.dependency_overrides`. No toca `horasclaras.db`.
- `Base.metadata.create_all` corre en el lifespan de la app, por eso el fixture de la DB tiene que estar creado antes de entrar al `TestClient`.
- `crear_cliente_payload()` centraliza el body válido. Agregá tests de reglas (409, 422, 404), no solo del happy path.

## Anti-alucinación

- No afirmes que un endpoint o test funciona sin ejecutarlo. Corré `pytest` y pegá la salida real.
- No inventes dependencias, comandos ni librerías. Verificá con `.\.venv\Scripts\python.exe -m pip freeze`.
- No uses `pip install` sueltas: cambiá `pyproject.toml` **y** `requirements.txt` juntos, y recreá el venv.
- No asumas Alembic, Docker, Redis, linters ni CI. No existen en este repo.
- Si una regla no está en este archivo ni en el código, preguntá antes de asumir.
- Antes de agregar campos o endpoints, chequeá si el dominio (tarifa por hora vs. por palabra) ya está resuelto en `entities/cliente.py`.

## Contexto de dominio

Dos tipos de cobro: `hora` (clases) y `palabra` (traducciones). `descuento_repeticion` es el porcentaje de descuento sobre las palabras REPETIDAS de un cliente por palabra (por defecto 50); ver "Reglas de dominio". El cálculo de horas/cobros todavía no está implementado: solo existe `clientes`.

## Reglas de dominio (fuente de verdad: propuesta del TP)

- Casos de uso: CU-01 registro/login, CU-02 alta de cliente, CU-03 registro de horas, CU-04 contador de palabras y presupuesto, CU-05 horas no facturables, CU-06 calculo del monto, CU-07 tarifario PDF, CU-08 dashboard mensual, CU-09 lista de espera, CU-10 asistente virtual.
- Maximo 10 clientes. Tarifa > 0. Descuento por repeticion 0..100, por defecto 50.
- Horas: solo clientes `hora`; minutos enteros > 0; tipo `facturable` o `planificacion` (esta ultima nunca se cobra).
- Monto por hora = minutos/60 x tarifa (solo facturables). Monto por palabra = (totales - repetidas) x tarifa + repetidas x tarifa x (1 - descuento/100).
- Calculos por cliente y por mes (YYYY-MM). El PDF no se guarda.
- Cada caso de uso se desarrolla con SDD: spec en `openspec/` antes del codigo. Hay skills en `.opencode/skills/` y un agente revisor en `.opencode/agents/`.
- MCP configurados en `opencode.json`: filesystem (interno, limitado a esta carpeta) y context7 (externo, documentacion de librerias).
- Ahorro de tokens: prompts en ingles, una sesion nueva por caso de uso, no pedir varios casos juntos.
