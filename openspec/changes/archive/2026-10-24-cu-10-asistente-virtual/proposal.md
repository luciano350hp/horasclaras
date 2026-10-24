# Proposal

> **Especificación retroactiva.** Este cambio se documentó el 2026-10-24, *después* de implementar y probar el caso de uso. Describe el comportamiento real verificado por los tests; no se escribió antes del código.

## Why

Que cualquier persona pueda preguntarle a un asistente cómo funciona la aplicación y sus reglas.

## What Changes

- `POST /api/chat` y `GET /api/chat/{conversation_id}`.
- RAG con LangChain + Chroma (base vectorial) + Groq sobre `knowledge/*.md`.
- Historial por conversación en SQLite.
- Pantalla de chat en el frontend.

## Capabilities

### New Capabilities

- `asistente`: ver `specs/asistente/spec.md`.

### Modified Capabilities

Ninguna.

## Impact

- Código: `app/services/chatbot_service.py`, `app/services/embeddings_hash.py`, `app/entities/mensaje_chat.py`, `app/controllers/chat_controller.py`, `knowledge/`, `frontend/src/pages/Asistente.jsx`.
- Pruebas: `tests/test_chat.py (8 tests)`.
