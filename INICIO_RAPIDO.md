# Inicio rápido — HorasClaras en 10 minutos (Windows + VS Code)

Una sola página, en orden. Hacé los pasos de arriba hacia abajo.

## Antes de empezar: qué tenés que tener instalado
- **Python** 3.11 o más (probá: `python --version`)
- **Node.js** (probá: `node --version`)
- **Git** (probá: `git --version`)

## Paso 1. Traer el proyecto actualizado
En VS Code: Archivo → Abrir carpeta → `C:\Users\Napo\Documents\HorasClaras`.
Menú Terminal → Nueva terminal. Corré:
```powershell
git fetch
git checkout cu-completos
git pull
```

## Paso 2. Instalar el servidor (una sola vez)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
Tarda unos minutos.

## Paso 3. Probar que todo está bien (opcional, 10 segundos)
```powershell
.\.venv\Scripts\python.exe -m pytest
```
Tiene que decir **76 passed**. Esto NO levanta la aplicación: solo corre pruebas y termina.

## Paso 4. Encender el servidor (terminal 1)
```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```
Tiene que decir `Application startup complete`. **Dejá esta terminal abierta.**
- La base de datos (`horasclaras.db`) se crea sola la primera vez. Empieza vacía.

## Paso 5. Encender las pantallas (terminal 2)
Abrí otra terminal con el botón **+** de la terminal de VS Code:
```powershell
cd frontend
npm install
npm run dev
```
**Dejá esta terminal abierta también.**

## Paso 6. Usar la aplicación
Abrí el navegador en **http://localhost:5173**

**No hay usuario creado de antemano.** La primera vez:
1. Tocá **"No tengo cuenta"**.
2. Escribí un email (puede ser inventado, por ejemplo `napo@mail.com`) y una contraseña de 6 o más caracteres.
3. Tocá **"Registrarme"**. Se crea la cuenta y entrás solo.

Después, probá en este orden: **Clientes** → **Horas** o **Traducciones** → **Cobro del mes** → **Dashboard** → **Tarifario PDF**.

## Paso 7 (opcional). Activar el asistente virtual
El asistente necesita una clave gratis de Groq. Sin ella, esa pestaña avisa que falta la clave y todo lo demás funciona igual.

1. Sacá la clave en https://console.groq.com/keys ("Create API Key").
2. En VS Code, en la lista de archivos de la izquierda, hacé clic derecho en un espacio vacío de la raíz (al lado de `README.md`) → Nuevo archivo → escribí `.env`.
3. Pegá adentro (con tu clave):
   ```
   GROQ_API_KEY=tu_clave
   ```
4. Guardá (`Ctrl + S`) y **reiniciá el servidor** (en la terminal 1: `Ctrl + C` y volvé a correr el comando del paso 4).
5. Abrí la pestaña **Asistente** y preguntá, por ejemplo: "¿Cuántos clientes puedo tener?". La primera pregunta tarda porque descarga un modelo.

⚠️ La clave va **solo** en `.env`. Nunca la pegues en otro archivo ni en un chat. El `.env` no se sube a GitHub.

## Si algo falla
| Síntoma | Qué hacer |
|---|---|
| `python` no se reconoce | Instalar Python y marcar "Add to PATH" |
| `npm` no se reconoce | Instalar Node.js |
| La pantalla carga pero da error de red | El servidor (terminal 1) no está encendido |
| El asistente dice "falta GROQ_API_KEY" | Falta el paso 7 o no reiniciaste el servidor |
| `pip install` falla con `chromadb` | Copiá el error completo y consultalo; el resto de la app no depende de eso |

## Para apagar todo
En cada terminal: `Ctrl + C`.
