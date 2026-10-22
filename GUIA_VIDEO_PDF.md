# Guion para video (10-15 minutos) + PDF de entrega

## VIDEO (10-15 min) - YouTube (sin listar) o Google Drive

### 1) Intro (1-1:30 min)
- Presentacion: nombre, apellido, proyecto "HorasClaras"
- Tema: sistema para profesoras/traductoras para gestionar horas, tarifas y calcular lo a facturar
- Explicar el objetivo: mostrar el entorno de IA mas que el codigo

### 2) AI Engineering - lo que el profe quiere ver (4-5 min)
Mostrar en VS Code:
- AGENTS.md (raiz) -> reglas globales, arquitectura 5 capas, convenciones
- app/AGENTS.md (nuevo) -> reglas especificas del backend
- .opencode/agents/ -> backend.md, frontend.md, revisor.md (explicar roles)
- .opencode/skills/ -> mostrar crear-caso-de-uso y reglas-tarifas (tuyas). Aclarar las 6 de OpenSpec
- opencode.json -> los 3 MCP del repo (filesystem, engram, context7) + aclarar memory es global
- openspec/changes/cu-03-registro-horas/ -> SDD: proposal, design, tasks, specs

Frase clave: ""Le enseñé a la IA cómo programar para este proyecto. Las reglas, las recetas y los agentes guían el trabajo.""

### 3) API funcionando (2-3 min)
Levantar servidor:
`powershell
cd C:\Users\Napo\Documents\HorasClaras
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
`
Abrir http://127.0.0.1:8000/docs
- Mostrar POST /api/clientes/ -> crear cliente (descuento default 50)
- Mostrar regla: intentar crear 11° cliente -> 409
- Mostrar POST /api/horas/ con cliente tipo palabra -> 422
- Decir: "Las reglas están en el service, no en el controller"

### 4) Tests + cierre (2-3 min)
En otra terminal:
`powershell
.\.venv\Scripts\python.exe -m pytest
`
Mostrar 44 passed
Abrir GitHub: https://github.com/luciano350hp/horasclaras
Mencionar: CU-02 y CU-03 hechos, faltan CU para llegar a 7, frontend React+Vite y chatbot LangChain+Groq pendientes.
Cerrar: "El foco fue armar el entorno asistido por IA para delegar bien el trabajo."

Duracion total: 10-14 minutos

## PDF DE ENTREGA

Portada
- Titulo: Trabajo Practico Integrador - HorasClaras
- Materia: IA Engineering / Arquitectura de Agentes
- Integrante: [Apellido y Nombre]
- Usuario GitHub: luciano350hp
- Repo: https://github.com/luciano350hp/horasclaras
- Video: [YouTube sin listar o Google Drive]

Contenido:
1) Tema y 10 casos de uso (marcar CU-02 y CU-03 como implementados)
2) Stack (Backend FastAPI/SQLAlchemy/SQLite, Frontend React+Vite, OpenCode+AGENTS+Skills+Agentes+OpenSpec, MCP, LangChain+Groq)
3) AI Engineering: explicar AGENTS.md, app/AGENTS.md, skills propias, agentes, SDD, MCP
4) Estado actual: 2/10 CU, 44 tests, todo subido
