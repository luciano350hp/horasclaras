# Spec Delta

## Purpose

CU-07: Las profesionales necesitan un documento prolijo con sus clientes y tarifas para enviar por WhatsApp o mail.

## ADDED Requirements

### Requirement: Generar el tarifario

The system SHALL generate a PDF listing every client with its modality, rate and repetition discount, without storing it.

#### Scenario: Con clientes

- **WHEN** existen clientes
- **THEN** responde 200 con `application/pdf` y el contenido empieza con `%PDF`

#### Scenario: Sin clientes

- **WHEN** no hay clientes
- **THEN** igual responde un PDF válido
