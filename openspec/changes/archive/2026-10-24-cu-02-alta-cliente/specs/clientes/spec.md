# Spec Delta

## Purpose

CU-02: Sin clientes no hay a quién registrarle horas ni traducciones. Es la base del dominio: cada cliente cobra por hora o por palabra.

## ADDED Requirements

### Requirement: Crear un cliente

The system SHALL allow creating a client with a unique name, a type (`hora` or `palabra`), a rate greater than zero and a repetition discount between 0 and 100 (default 50).

#### Scenario: Alta exitosa

- **WHEN** se envía un cliente válido
- **THEN** responde 201 y devuelve el cliente con su id

#### Scenario: Descuento por defecto

- **WHEN** no se envía `descuento_repeticion`
- **THEN** se guarda con 50

#### Scenario: Nombre duplicado

- **WHEN** se envía un nombre ya existente
- **THEN** responde 409

#### Scenario: Nombre vacío o solo espacios

- **WHEN** el nombre queda vacío tras quitar espacios
- **THEN** responde 422 y no persiste nada

#### Scenario: Datos inválidos

- **WHEN** la tarifa es negativa, el tipo no existe o el descuento está fuera de 0–100
- **THEN** responde 422

### Requirement: Límite de clientes

The system MUST NOT allow more than 10 clients.

#### Scenario: Cliente número 11

- **WHEN** ya existen 10 clientes
- **THEN** responde 409

#### Scenario: Liberar lugar

- **WHEN** se elimina un cliente existente
- **THEN** se puede crear uno nuevo

### Requirement: Consultar y modificar clientes

The system SHALL list, read, partially update and delete clients.

#### Scenario: Cliente inexistente

- **WHEN** se pide, modifica o borra un id que no existe
- **THEN** responde 404

#### Scenario: Actualización parcial

- **WHEN** se envían solo algunos campos
- **THEN** solo cambian esos campos

#### Scenario: Renombrar a un nombre existente

- **WHEN** se actualiza el nombre a uno ya usado
- **THEN** responde 409
