# HorasClaras — Documentación completa

Este documento explica **todo el proyecto en lenguaje simple**: qué es, cómo se usa, cómo está hecho por dentro, cómo se construyó con IA y qué falta. Está pensado para que lo lea alguien que no programa.

**Índice**
1. [Qué es HorasClaras](#1-qué-es-horasclaras)
2. [Qué puede hacer: los 10 casos de uso](#2-qué-puede-hacer-los-10-casos-de-uso)
3. [Cómo está hecho por dentro](#3-cómo-está-hecho-por-dentro)
4. [Reglas de negocio](#4-reglas-de-negocio)
5. [Cómo instalarlo y usarlo (Windows)](#5-cómo-instalarlo-y-usarlo-windows)
6. [Qué es el archivo `.env`](#6-qué-es-el-archivo-env)
7. [Tests](#7-tests)
8. [El asistente virtual](#8-el-asistente-virtual)
9. [Cómo se trabajó con IA](#9-cómo-se-trabajó-con-ia)
10. [Mapa de carpetas](#10-mapa-de-carpetas)
11. [Límites conocidos y qué falta](#11-límites-conocidos-y-qué-falta)
12. [Glosario](#12-glosario)
13. [Otros documentos](#13-otros-documentos)

---

## 1. Qué es HorasClaras

Una aplicación web para **profesoras de inglés y traductoras freelance**. Resuelve tres problemas:

- A fin de mes no saben cuántas horas trabajaron para cada cliente.
- Calcular cuánto cobrar a mano (con descuentos por palabras repetidas) es lento y se presta a errores.
- No distinguen el tiempo que cobran del tiempo de planificación que no cobran.

La aplicación registra horas y traducciones, calcula el monto a cobrar por cliente y por mes, muestra un resumen y genera un tarifario en PDF.

## 2. Qué puede hacer: los 10 casos de uso

Un **caso de uso (CU)** es una cosa concreta que la persona puede hacer con la aplicación.

| CU | Qué hace | Pestaña de la app | Dirección del servidor |
|---|---|---|---|
| CU-01 | Crear una cuenta e iniciar sesión | Pantalla de ingreso | `/api/auth/registro`, `/api/auth/login`, `/api/auth/me` |
| CU-02 | Dar de alta, ver y borrar clientes (hasta 10) | Clientes | `/api/clientes/` |
| CU-03 | Registrar las horas trabajadas | Horas | `/api/horas/` |
| CU-04 | Registrar traducciones: palabras totales y repetidas | Traducciones | `/api/traducciones/` |
| CU-05 | Marcar horas como "planificación" (no se cobran) | Horas | `/api/horas/` (tipo `planificacion`) |
| CU-06 | Calcular cuánto cobrar por cliente y por mes | Cobro del mes | `/api/calculos/AAAA-MM` |
| CU-07 | Descargar el tarifario en PDF | Tarifario PDF | `/api/tarifario/pdf` |
| CU-08 | Ver el resumen del mes (totales, mejor cliente, gráfico) | Dashboard | `/api/dashboard/AAAA-MM` |
| CU-09 | Dejar el email en una lista de espera | Lista de espera | `/api/waitlist` |
| CU-10 | Preguntarle al asistente virtual cómo funciona la app | Asistente | `/api/chat` |

## 3. Cómo está hecho por dentro

Una aplicación web tiene tres partes. Acá se llaman así:

- **El frontend** es lo que la persona ve y toca en el navegador: botones, formularios, tablas. Está hecho con **React** y **Vite**, y vive en la carpeta `frontend/`.
- **El backend** (también "la API" o "el servidor") es el programa que recibe los pedidos del frontend, hace las cuentas y guarda los datos. Está hecho con **Python y FastAPI**, y vive en la carpeta `app/`. La **API** es la lista de direcciones (como `/api/clientes/`) a las que el frontend le hace pedidos.
- **La base de datos** es donde quedan guardados los datos, para que no se pierdan al cerrar el programa. Es un solo archivo llamado `horasclaras.db`, de tipo **SQLite**.

```
Navegador (React)  ──pedido──▶  Servidor (FastAPI)  ──lee y escribe──▶  Base de datos (SQLite)
   localhost:5173   ◀─respuesta─   localhost:8000                          horasclaras.db
```

### Las tablas de la base de datos

Una **tabla** es como una planilla de Excel: cada columna es un dato y cada fila es un registro.

| Tabla | Qué guarda |
|---|---|
| `clientes` | Nombre, tipo (hora o palabra), tarifa y descuento por repetición |
| `horas` | Fecha, minutos, tipo (facturable o planificación), observación, y a qué cliente pertenecen |
| `traducciones` | Fecha, palabras totales, palabras repetidas, y a qué cliente pertenecen |
| `usuarios` | Email y contraseña (guardada cifrada, nunca en texto) |
| `suscripciones` | Emails de la lista de espera |
| `mensajes_chat` | Historial de cada conversación con el asistente |

Además, el asistente tiene su propia base **vectorial** (Chroma, carpeta `data/chroma`), explicada en la sección 8.

### Las capas del backend

Para que el código sea ordenado, cada pedido pasa por cinco capas. Cada capa hace una sola cosa, igual que en un restaurante:

| Capa | Carpeta | Qué hace | En el restaurante |
|---|---|---|---|
| Controller | `app/controllers/` | Recibe el pedido y devuelve la respuesta | El mozo |
| DTO | `app/dtos/` | Define y valida la forma de los datos | La comanda |
| Service | `app/services/` | Aplica las reglas de negocio y hace las cuentas | El cocinero |
| Repository | `app/repositories/` | Es la única que habla con la base de datos | El que busca en la despensa |
| Entity | `app/entities/` | Describe cada tabla | El estante de la despensa |

Ejemplo: cuando se crea un cliente, el controller recibe el pedido, el DTO verifica que los datos sean válidos, el service comprueba que no haya ya 10 clientes, y el repository lo guarda usando la entity.

## 4. Reglas de negocio

- Un cliente es **por hora** o **por palabra**.
- Máximo **10 clientes**. El 11.º se rechaza.
- **Monto por hora** = minutos facturables ÷ 60 × tarifa.
- Las horas de **planificación nunca se cobran**, pero se muestran.
- **Monto por palabra** = (palabras totales − repetidas) × tarifa + repetidas × tarifa × (1 − descuento ÷ 100).
- El **descuento por repetición** va de 0 a 100 y vale **50** si no se indica. Solo afecta a las palabras repetidas.
- Las palabras repetidas no pueden superar a las totales.
- Horas solo se cargan a clientes por hora; traducciones solo a clientes por palabra.
- El cobro se calcula por **mes** (formato `2026-05`). Un mes sin movimientos da 0.
- El PDF se genera al momento y **no se guarda**.
- El dinero se calcula con `Decimal` (no con decimales comunes) para que no haya errores de centavos.

Ejemplo: 1000 palabras, 400 repetidas, tarifa 0,10, descuento 50 %. Palabras nuevas: 600 × 0,10 = 60. Repetidas: 400 × 0,10 × 0,5 = 20. Total: **80**.

## 5. Cómo instalarlo y usarlo (Windows)

Requisitos: Python 3.11 o más, Node.js y Git instalados.

**Primera vez**
```powershell
git clone https://github.com/luciano350hp/horasclaras
cd horasclaras
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
cd frontend
npm install
cd ..
```

**Cada vez que quieras usarlo** (se usan dos ventanas de PowerShell)

Ventana 1, el servidor:
```powershell
cd horasclaras
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Ventana 2, las pantallas:
```powershell
cd horasclaras\frontend
npm run dev
```

Abrí http://localhost:5173 en el navegador. Registrate, creá un cliente y probá las pestañas. La documentación interactiva del servidor está en http://127.0.0.1:8000/docs.

## 6. Qué es el archivo `.env`

El `.env` es un archivo de texto con **configuraciones privadas** de tu computadora, sobre todo **contraseñas y claves**. Se llama así por "environment" (entorno). El programa lo lee al arrancar.

Por eso **no se sube a GitHub**: si lo subieras, cualquiera vería tus claves. Está en el `.gitignore` (la lista de lo que Git ignora). En su lugar se sube `.env.example`, una **plantilla sin los valores secretos**, para que cada persona cree el suyo.

Para crear el tuyo, copiá `.env.example` como `.env` y completalo:

```
DATABASE_URL=sqlite:///./horasclaras.db
GROQ_API_KEY=tu_clave_de_groq
GROQ_MODEL=openai/gpt-oss-20b
```

| Variable | Para qué sirve | Si falta |
|---|---|---|
| `DATABASE_URL` | Dónde está la base de datos | Usa `horasclaras.db` en la carpeta del proyecto |
| `GROQ_API_KEY` | Clave para que el asistente use Groq. Se saca gratis en console.groq.com | El asistente responde que falta la clave; el resto anda |
| `GROQ_MODEL` | Qué modelo de Groq usar | Usa `openai/gpt-oss-20b` |
| `EMBEDDINGS_BACKEND` | `fastembed` (por defecto) o `hash` (sin descargas) | Usa `fastembed` |
| `SECRET_KEY` | Firma las sesiones de login. Cambiala en un uso real | Usa un valor de desarrollo |

## 7. Tests

Un **test** es un programa corto que prueba que otra parte del programa funcione. Hay 76. Cubren el caso feliz y los errores (404 no existe, 409 duplicado, 422 datos inválidos, 401 sin permiso).

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Tiene que decir `76 passed`. Los tests usan una base de datos temporal en memoria, así que **no tocan tus datos**. El asistente se prueba con un modelo falso, así que no gasta cuota de Groq.

## 8. El asistente virtual

Responde preguntas sobre cómo funciona la aplicación. Usa una técnica llamada **RAG** (generación con recuperación):

1. Los documentos de la carpeta `knowledge/` se cortan en fragmentos.
2. Cada fragmento se convierte en una lista de números que representa su significado (un **embedding**) y se guarda en una **base de datos vectorial** (**Chroma**).
3. Cuando alguien pregunta, se busca en esa base los 4 fragmentos más parecidos a la pregunta.
4. Esos fragmentos, junto con los últimos mensajes de la conversación, se mandan a un **modelo de lenguaje** (Groq) con la instrucción de responder solo con esa información.
5. La conversación se guarda en SQLite con un `conversation_id`.

**LangChain** es la librería que conecta todas estas piezas. Si no hay clave de Groq, el servidor responde con un aviso claro (error 503). Si el modelo de embeddings no se puede descargar, usa un plan B local, menos preciso.

Para ampliar lo que sabe el asistente, se agregan archivos `.md` en `knowledge/` y se borra la carpeta `data/chroma` para que se vuelva a indexar.

## 9. Cómo se trabajó con IA

El curso evalúa trabajar con un **entorno asistido por IA**. Estas son las piezas:

| Pieza | Qué es | Dónde está |
|---|---|---|
| **OpenCode** | El programa donde se conversa con la IA para que escriba y revise código | Se abre en la carpeta del proyecto |
| **`AGENTS.md`** | Las "reglas de la casa" que la IA lee siempre antes de actuar | `AGENTS.md` (general), `app/AGENTS.md` (backend) y `frontend/AGENTS.md` (frontend) |
| **Skills** | Instrucciones paso a paso para tareas repetibles, como "crear un caso de uso" | `.opencode/skills/` |
| **Agentes** | IAs con un rol y permisos propios. `revisor` solo lee y audita; `backend` y `frontend` escriben | `.opencode/agents/` |
| **Comandos** | Atajos para el flujo de OpenSpec (`/opsx-propose`, etc.) | `.opencode/commands/` |
| **MCP** | Conectores que le dan a la IA acceso a herramientas: `filesystem` (archivos), `context7` (documentación de librerías), `engram` (memoria) | `opencode.json` |
| **SDD con OpenSpec** | **Desarrollo guiado por especificación**: primero se escribe qué tiene que hacer cada caso de uso y después se programa | `openspec/` |

El flujo de OpenSpec es: **proponer** un cambio (qué y por qué) → escribir su **especificación** (requisitos y escenarios) → **implementar** con la lista de tareas → **archivar** el cambio terminado.

**Gentle AI** es un paquete opcional que había inyectado 13 agentes en `opencode.json` y lo hacía pesar 125 KB. Consumía muchísimo contexto, así que se **sacó**: el archivo quedó en menos de 1 KB.

### Cómo se construyó realmente

- **Con OpenCode y OpenSpec:** el setup de IA, CU-02 (clientes) y CU-03 (horas, con su especificación en `openspec/changes/cu-03-registro-horas/`).
- **Con Claude (asistente de chat), directamente sobre el código:** CU-01 y CU-04 a CU-10, el frontend completo y el asistente virtual, después de que el cupo gratuito de OpenCode se agotó. Estos casos de uso no pasaron por OpenSpec.

Esta distinción se deja escrita a propósito, para que el trabajo sea transparente.

## 10. Mapa de carpetas

```
horasclaras/
├── AGENTS.md              Reglas para la IA (generales)
├── README.md              Presentación del proyecto
├── opencode.json          Configuración de OpenCode y MCP
├── requirements.txt       Lista de librerías de Python
├── .env.example           Plantilla de configuración (el .env real no se sube)
├── app/                   BACKEND (servidor)
│   ├── AGENTS.md          Reglas de la IA para el backend
│   ├── main.py            Arranque del servidor
│   ├── controllers/       Capa 1: recibe pedidos
│   ├── dtos/              Capa 2: valida datos
│   ├── services/          Capa 3: reglas y cuentas
│   ├── repositories/      Capa 4: habla con la base
│   ├── entities/          Capa 5: describe las tablas
│   └── core/              Configuración y conexión a la base
├── frontend/              FRONTEND (pantallas React)
│   ├── AGENTS.md          Reglas de la IA para el frontend
│   └── src/pages/         Una pantalla por caso de uso
├── knowledge/             Documentos que lee el asistente
├── tests/                 Pruebas automáticas
├── openspec/              Especificaciones (SDD)
├── .opencode/             Skills, agentes y comandos de OpenCode
└── docs/                  Documentación (este archivo y la del producto)
    └── producto/          PRD, modelo de datos y preguntas del bot
```

## 11. Límites conocidos y qué falta

- **El login no protege el resto de la app.** Se puede crear cuenta e ingresar, pero los clientes, horas y cobros no están separados por usuario: todos ven los mismos datos. Para un uso real habría que asociar cada dato a su dueño.
- **El servidor acepta pedidos de cualquier origen** (CORS abierto). Está bien para desarrollo; en producción se restringe.
- **La base es SQLite**, un solo archivo. Alcanza para una persona; para muchas usuarias se pasaría a PostgreSQL.
- **El asistente no ve tus datos.** Solo explica cómo funciona la app.
- **Faltan las especificaciones de OpenSpec** de los CU construidos sin OpenSpec, y archivar el cambio de CU-03.
- **Pendiente de probar en la computadora del autor:** el asistente con una clave real de Groq y el modelo de embeddings multilingüe.

## 12. Glosario

| Palabra | Qué significa |
|---|---|
| **API** | La lista de direcciones a las que el frontend le pide cosas al servidor |
| **Backend** | El servidor: hace las cuentas y guarda datos |
| **Frontend** | Las pantallas que ve la persona |
| **Base de datos** | Donde se guardan los datos de forma permanente |
| **Tabla** | Una "planilla" dentro de la base de datos |
| **Endpoint** | Una dirección concreta de la API, como `/api/clientes/` |
| **DTO** | Molde que define cómo tienen que venir los datos |
| **Test** | Programa que verifica que otro programa funcione |
| **`.env`** | Archivo privado con claves y configuración |
| **MCP** | Conector que le da herramientas a la IA |
| **SDD / OpenSpec** | Escribir la especificación antes que el código |
| **RAG** | Que la IA busque en tus documentos antes de responder |
| **Embedding** | Un texto convertido a números que representan su significado |
| **Base vectorial** | Base de datos que busca por parecido de significado |
| **LangChain** | Librería que conecta modelo, documentos y base vectorial |
| **Groq** | Servicio que ejecuta el modelo de lenguaje del asistente |
| **Git / GitHub** | Sistema que guarda el historial del proyecto y sitio donde se publica |
| **Rama (branch)** | Una copia paralela del proyecto para probar cambios sin romper la principal |

## 13. Otros documentos

- [`docs/producto/PRD.md`](producto/PRD.md): definición del producto: problema, usuaria, funcionalidades, métricas y restricciones.
- [`docs/producto/DER.md`](producto/DER.md): modelo de datos propuesto (diagrama).
- [`docs/producto/QA_bot.md`](producto/QA_bot.md): preguntas y respuestas de la versión prototipo (Lovable).
- [`AGENTS.md`](../AGENTS.md) y [`app/AGENTS.md`](../app/AGENTS.md) y [`frontend/AGENTS.md`](../frontend/AGENTS.md): reglas para la IA, en jerarquía (general + backend + frontend).
- [`README.md`](../README.md): resumen técnico y guía de arranque.
- [`GUIA_VIDEO_PDF.md`](../GUIA_VIDEO_PDF.md): guion del video de entrega.
