# Demo HorasClaras — Guion para la clase

**TP: IA Engineering — Cohorte 2, UNLa**
**Alumno: Luciano Napoleone**
**Repo: https://github.com/luciano350hp/horasclaras**

---

## Lo que dice el profe que se evalúa en la demo

Texual del material de clases:

> *"Demos: semana del 20/10. No son obligatorias. Se muestra lo que tengas hecho, **sobre todo cómo armaste el setup**."* (Clase 2)

> *"Se evalúa mucho el **setup del agente** (cómo lo pensaste y lo armaste), **más que la calidad del código**."* (Clase 2)

> *"Sí se miran cuestiones críticas de seguridad: no exponer credenciales de la base ni de APIs."* (Clase 2)

**Conclusión: la demo NO es sobre cuántos casos de uso andan. Es sobre el entorno de IA que armaste.** Ese es el mensaje central.

---

## Puntaje oficial del TP (Clase 3)

| # | Qué se evalúa | Puntos |
|---|---|---|
| 1 | Funcionalidad: ≥7 de 10 casos de uso | hasta 3 |
| 2 | Esquema de trabajo y AI Engineering (AGENTS.md, skills, SDD) | hasta 3 |
| 3 | README: arquitectura, 10 CU, prompts, iteraciones, MCP | hasta 1 |
| 4 | MCP: mínimo 2, al menos 1 externo | hasta 1 |
| 5 | Chatbot LangChain integrado en la web | hasta 2 |

**Aprueba con 7/10.** En la demo mostramos los puntos **2, 3 y 4** (que ya están completos) y un avance del **1**.

---

## ANTES DE EMPEZAR: cómo se levanta el "servidor" (leer esto primero)

**¿Qué es el servidor?** El backend de HorasClaras no es una app con ventana. Es un **programa que se queda escuchando** en tu PC, esperando pedidos web. Mientras está encendido, la dirección `http://127.0.0.1:8000/docs` funciona. Si está apagado, esa dirección **no existe** y el navegador da error. **Ese es el "servidor".**

**¿Dónde se escribe el comando?** En una **consola de PowerShell**. Para abrir una: tecla **Windows + R** → escribí `powershell` → Enter. O si ya tenés OpenCode abierto, usá su terminal.

**Paso a paso:**

1. Abrí la consola y **entrá a la carpeta del proyecto**:
   ```powershell
   cd C:\Users\Napo\Documents\HorasClaras
   ```

2. **Encendé el servidor** con este comando:
   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
   ```

3. Vas a ver esto y **se va a quedar ahí** (no se cuelga, está funcionando):
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000  (Press CTRL+C to quit)
   INFO:     Application startup complete.
   ```

4. **NO cierres esa consola.** Dejala abierta. Ahora, en el **navegador**, abrí:
   ```
   http://127.0.0.1:8000/docs
   ```

5. Cuando termines la demo, para apagarlo: en esa consola apretá **`Ctrl + C`**.

**Si `/docs` no anda:** es porque el paso 2 no está corriendo. La causa #1 es que la consola no está en la carpeta del proyecto (paso 1). La causa #2 es que cerraste la consola o apretaste `Ctrl + C`. Volvé a encenderlo.

---

## Estructura de la demo (5 minutos)

### 1. Apertura — la frase que resume todo (15 seg)

> *"HorasClaras es un sistema para que profesoras de idiomas y traductoras gestionen horas y tarifas. Backend en FastAPI, base SQLite. Lo importante de este TP no es el código, es **cómo armé el entorno de IA para que la IA lo programara**: reglas de contexto, skills, agentes y especificaciones antes del código."*

### 2. La app funciona — `/docs` en vivo (60 seg)

**Primero encendé el servidor** (si no lo hiciste, ver la sección "ANTES DE EMPEZAR" arriba):

```powershell
cd C:\Users\Napo\Documents\HorasClaras
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Después abrí el navegador** en **http://127.0.0.1:8000/docs**

Demostrar en vivo (3 acciones):
1. Crear un cliente de tipo `hora` → devuelve **201**
2. Cargarle una hora de 60 minutos → devuelve **201**
3. **Mostrar un error a propósito**: cargar una hora a un cliente de tipo `palabra` → devuelve **422**

> *"Ese 422 no está en el controller: es una regla de negocio que vive en el service. Solo se registran horas para clientes por hora."*

### 3. Los tests (20 seg)

```powershell
.\.venv\Scripts\python.exe -m pytest
```

> *"44 tests en verde: 27 de clientes y 14 de horas. Cubren el caso feliz y los errores 404, 409 y 422."*

### 4. El setup de IA — **EL CORAZÓN DE LA DEMO** (2 min)

Abrir cada archivo y explicar en una línea:

| Abrir | Decir |
|---|---|
| `AGENTS.md` | *"El manual que la IA lee siempre: stack con versiones exactas, la arquitectura de 5 capas, convenciones y reglas anti-alucinación. Está en la raíz, que es la zona de mayor retención del contexto."* |
| `.opencode/skills/crear-caso-de-uso/SKILL.md` | *"Una skill: el procedimiento paso a paso para agregar un caso de uso. Se carga sola solo cuando el pedido lo necesita, así no llena la ventana de contexto."* |
| `.opencode/skills/reglas-tarifas/SKILL.md` | *"Otra skill, con las fórmulas de cobro. Separadas del AGENTS.md para no hacerlo gigante."* |
| `.opencode/agents/revisor.md` | *"Un agente auditor. Tiene `edit: deny` y `bash: deny`: puede revisar el código pero **no puede modificarlo**. Ese es el control de calidad."* |
| `opencode.json` | *"Los MCP: `filesystem` interno, limitado a esta carpeta, y `context7` **externo**, que consulta documentación actualizada de FastAPI para no usar APIs viejas."* |
| `openspec/` | *"Y esto es el SDD: la especificación de cada caso de uso **antes** de programarlo. Acá está el cambio `cu-03-registro-horas` con proposal, specs, design y tasks."* |
| `.aisignore` + `.gitignore` | *"El firewall de contexto: dejan afuera `.env`, la base `.db`, el `.venv`. Nada sensible se indexa ni se sube a GitHub."* |

### 5. El flujo SDD en concreto (60 seg)

Mostrar `openspec/changes/cu-03-registro-horas/` y recorrer los 4 archivos:

> *"Cada caso de uso pasa por este flujo, en este orden, **antes de escribir código**:*
> 1. `proposal.md` — qué se hace y por qué
> 2. `specs/horas/spec.md` — los requisitos con escenarios 'cuando… entonces…'
> 3. `design.md` — las decisiones técnicas y las alternativas que descarté
> 4. `tasks.md` — los pasos, cada uno con su forma de verificación
>
> *Recién después va el código. Y al final se valida con `openspec validate --strict`."*

### 6. Cierre (20 seg)

> *"En GitHub está todo: el repo `luciano350hp/horasclaras`, con el README que documenta la arquitectura, los 10 casos de uso, los prompts que usé, los problemas que resolví y la configuración de los MCP. El setup de IA está completo; seguimos sumando casos de uso y el chatbot LangChain."*

---

## Lo que NO hay que decir ni mostrar

- **No** decir que faltan casos de uso como si fuera un error grave. Se muestra lo que hay y se dice *"seguimos sumando"*.
- **No** mostrar `horasclaras.db` ni `.env`. No existen en GitHub (están ignorados), así que si abrís el repo remoto no aparecen.
- **No** actualizar OpenCode (el profe lo pidió explícitamente hasta terminar el proyecto).
- **No** entrar en detalles de performance ni buenas prácticas: **no se evalúan**.

---

## Checklist antes de la demo

```powershell
# 1. Ver que los tests pasen (mostrar la salida real)
.\.venv\Scripts\python.exe -m pytest

# 2. Levantar el servidor
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload

# 3. Abrir la doc interactiva
#    http://127.0.0.1:8000/docs

# 4. Verificar que el repo esté subido y al día
git status -sb
gh repo view --web
```

---

## Puntos clave que el profe pidió tener listos (según las clases)

- [x] **AGENTS.md** con stack, arquitectura y reglas anti-alucinación (Clase 2)
- [x] **Skills** en `.opencode/skills/` (Clase 2)
- [x] **Agentes** en `.opencode/agents/` con permisos propios (Clase 2)
- [x] **MCP**: mínimo 2, al menos 1 externo — context7 es externo (Clase 5)
- [x] **`.aisignore` / `.gitignore`** con `.env`, `.venv`, `*.db` (Clase 3)
- [x] **SDD con OpenSpec**: spec antes del código (Clase 3)
- [x] **README** con arquitectura, 10 CU, prompts, iteraciones y MCP (Clase 3)
- [x] **Repo en GitHub** para que los profes lo descarguen (Clase 6)
- [ ] Chatbot LangChain (se hace al final, vale 2 puntos)
- [ ] Frontend (obligatorio para la entrega final del 27/10)

---

## Frases de respaldo (por si preguntan)

- **¿Por qué capas?** *"Para que cada parte tenga una sola responsabilidad y poder testear sin tocar HTTP. El controller no toca la base; si hace falta una consulta nueva va en el repository y una regla nueva va en el service."*
- **¿Por qué SDD y no pedirle código directo a la IA?** *"Sin especificación la IA infiere, y ahí se equivoca en nombres de campos y en reglas de negocio. Con el SDD la spec es la fuente de verdad y después se verifica el código contra ella."*
- **¿Por qué dos MCP?** *"filesystem para que el agente lea y escriba solo dentro del proyecto, y context7 externo para consultar documentación actualizada de las librerías en vez de que alucine APIs viejas."*
- **¿Qué pasa si dos reglas chocan?** *"La herramienta te pide que decidas. Por eso el AGENTS.md tiene que estar sólido antes de sumar SDD."*
- **¿El código lo escribiste vos?** *"Casi todo lo escribió el agente en modo Plan/Build. Mi rol fue diseñar la arquitectura, definir las reglas, escribir las specs y auditar lo que devolvía."*
