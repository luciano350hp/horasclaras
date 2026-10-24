# AGENTS.md (Frontend)

Este archivo aplica **únicamente** al código dentro de `frontend/`. Para reglas globales ver `../AGENTS.md`; para el servidor, `../app/AGENTS.md`.

## Alcance
- Trabajar solo en `frontend/src/`.
- NO tocar `app/`, `tests/`, `.opencode/`, `openspec/` ni MCP sin pedido explícito.
- Si hace falta un endpoint nuevo, pedirlo: no inventar rutas ni cambiar el contrato del backend.

## Stack
- React 18 + Vite 5, JavaScript (`.jsx`). Sin router externo ni librerías de UI: una pestaña por caso de uso en `App.jsx`.
- Estilos en `src/styles.css` (variables CSS). No agregar Tailwind ni frameworks sin pedirlo.
- Idioma de la UI: **español rioplatense** (voseo: "cargás", "elegís"). Nunca inglés ni español neutro en textos de usuario.

## Estructura
```
src/
├── main.jsx        punto de entrada
├── App.jsx         login + navegación por pestañas
├── api.js          ÚNICO lugar que hace fetch al backend
├── hooks.js        useLista, formateo de dinero y mes
└── pages/          una pantalla por caso de uso
```

## Reglas
- Todo pedido HTTP va por `src/api.js`. Las páginas no llaman a `fetch` directo.
- La URL del backend sale de `VITE_API_URL` (por defecto `http://127.0.0.1:8000`). No hardcodear otra.
- **Dinero:** el backend manda decimales como string. Nunca recalcular montos en el frontend: mostrar lo que devuelve `/api/calculos` y `/api/dashboard`. Solo formatear.
- Mostrar siempre el mensaje de error que devuelve la API (`detail`); no tragarse errores.
- Los formularios validan lo básico (`required`, `min`), pero la validación real es la del backend.
- El token de login vive en `localStorage` (`token`). No guardar otros datos sensibles ahí.
- Cada página nueva: agregar el archivo en `pages/`, registrar la pestaña en `App.jsx` y el método en `api.js`.

## Comandos
```powershell
cd frontend
npm install
npm run dev      # http://localhost:5173 (el backend tiene que estar en :8000)
npm run build    # verifica que compila
```

## Flujo
1. Usar OpenSpec si es un caso de uso nuevo (`openspec/changes/<id>/`).
2. Implementar la pantalla siguiendo la estructura de arriba.
3. Correr `npm run build` y probar a mano contra el backend real.
4. No commitear sin pedido.
