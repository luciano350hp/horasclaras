# Spec Delta

## Purpose

CU-10: Que cualquier persona pueda preguntarle a un asistente cómo funciona la aplicación y sus reglas.

## Requirements

### Requirement: Responder preguntas con la documentación

The system SHALL answer a question using the most similar documentation fragments retrieved from the vector store.

#### Scenario: Pregunta cubierta por la documentación

- **WHEN** se pregunta cuántos clientes se pueden tener
- **THEN** el contexto enviado al modelo contiene la regla de los 10 clientes y la respuesta indica sus fuentes

#### Scenario: Mensaje vacío

- **WHEN** el mensaje está vacío
- **THEN** responde 422

### Requirement: Mantener la conversación

The system SHALL keep the history of each conversation by `conversation_id`.

#### Scenario: Seguimiento

- **WHEN** se envía un segundo mensaje con el mismo `conversation_id`
- **THEN** el turno anterior viaja al modelo y el historial guarda 4 mensajes

#### Scenario: Conversaciones separadas

- **WHEN** se inician dos conversaciones
- **THEN** cada una tiene su propio historial

### Requirement: Fallar de forma clara

The system MUST report configuration or provider errors with a clear message.

#### Scenario: Falta la clave

- **WHEN** no hay `GROQ_API_KEY`
- **THEN** responde 503 mencionando `GROQ_API_KEY`

#### Scenario: Falla el proveedor

- **WHEN** el modelo lanza un error
- **THEN** responde 502
