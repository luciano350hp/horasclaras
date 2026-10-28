# Spec Delta

## Purpose

CU-11: La traductora pega un texto y obtiene el conteo de palabras, las repeticiones y el precio para un cliente por palabra.

## Requirements

### Requirement: Presupuestar un texto

The system SHALL count the words of the given text, detect exact repeated segments, and compute the price for a client of type `palabra` using the client's rate and repetition discount.

#### Scenario: Presupuesto sin repeticiones

- **WHEN** se envía un texto sin segmentos repetidos para un cliente por palabra
- **THEN** responde 200 con `palabras_repetidas` en 0 y `monto` igual a palabras × tarifa

#### Scenario: Presupuesto con una frase repetida

- **WHEN** el texto contiene una frase exacta dos veces
- **THEN** las palabras de la segunda aparición se cuentan como repetidas y se les aplica el descuento

#### Scenario: Cliente por hora

- **WHEN** el cliente es de tipo `hora`
- **THEN** responde 422

#### Scenario: Cliente inexistente

- **WHEN** el `cliente_id` no existe
- **THEN** responde 404

#### Scenario: Texto vacío

- **WHEN** el texto está vacío o solo tiene espacios
- **THEN** responde 422

### Requirement: No persistir

The system SHALL NOT store anything when computing a quote.
