# Spec Delta

## Purpose

CU-04: Las traductoras cobran por palabra y necesitan registrar cuántas palabras tuvo cada trabajo y cuántas eran repetidas.

## ADDED Requirements

### Requirement: Registrar una traducción

The system SHALL allow registering a translation job for a client of type `palabra`, with total words greater than zero and repeated words between 0 and the total.

#### Scenario: Registro exitoso

- **WHEN** se envía un trabajo válido para un cliente por palabra
- **THEN** responde 201

#### Scenario: Repetidas mayores que totales

- **WHEN** `palabras_repetidas` supera a `palabras_totales`
- **THEN** responde 422

#### Scenario: Cliente inexistente

- **WHEN** el `cliente_id` no existe
- **THEN** responde 404

#### Scenario: Cliente por hora

- **WHEN** el cliente es de tipo `hora`
- **THEN** responde 422

### Requirement: Consultar y borrar traducciones

The system SHALL list, read and delete translation jobs.

#### Scenario: Ciclo completo

- **WHEN** se listan, obtienen y borran trabajos
- **THEN** el borrado responde 204 y luego el trabajo da 404
