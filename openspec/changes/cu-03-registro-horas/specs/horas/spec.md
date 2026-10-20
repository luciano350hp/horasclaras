# Spec Delta

## Purpose

Permite registrar las horas que una profesora dicta a cada cliente de tipo `hora`, distinguiendo las horas facturables de las de planificación, para que el cálculo del monto (CU-06) y el tarifario (CU-07) tengan de dónde leer.

## ADDED Requirements

### Requirement: Registrar una hora

The system SHALL allow registering worked hours for a client whose type is `hora`. The registration MUST record the client, the date, the duration in whole minutes, and whether the time is billable or planning.

#### Scenario: Registro exitoso

- **WHEN** se envía una hora válida para un cliente de tipo `hora`
- **THEN** el sistema responde 201 y persiste el registro con su id

#### Scenario: El cliente no existe

- **WHEN** se envía una hora con un `cliente_id` inexistente
- **THEN** el sistema responde 404 y no persiste nada

#### Scenario: El cliente no es de tipo hora

- **WHEN** se envía una hora para un cliente de tipo `palabra`
- **THEN** el sistema responde 422 y no persiste nada

#### Scenario: Minutos no positivos o no enteros

- **WHEN** se envía `minutos` con valor 0, negativo o no entero
- **THEN** el sistema responde 422

#### Scenario: Tipo de hora inválido

- **WHEN** se envía `tipo` con un valor distinto de `facturable` o `planificacion`
- **THEN** el sistema responde 422

### Requirement: Listar horas

The system SHALL list registered hours, optionally filtered by client.

#### Scenario: Listado exitoso

- **WHEN** se pide el listado de horas
- **THEN** el sistema responde 200 con las horas registradas

#### Scenario: Listado filtrado por cliente

- **WHEN** se pide el listado con un filtro de cliente
- **THEN** el sistema devuelve únicamente las horas de ese cliente

### Requirement: Obtener y eliminar una hora

The system SHALL allow fetching a single hour by id and deleting it, returning 404 when the hour does not exist.

#### Scenario: Obtener una hora existente

- **WHEN** se pide una hora por su id existente
- **THEN** el sistema responde 200 con esa hora

#### Scenario: Operar sobre una hora inexistente

- **WHEN** se pide o se elimina una hora con id inexistente
- **THEN** el sistema responde 404

### Requirement: La planificación nunca se factura

The system SHALL store planning hours with the same validity as billable hours, so they can be reported separately but never counted as billable.

#### Scenario: Una hora de planificación se registra igual

- **WHEN** se registra una hora con `tipo` igual a `planificacion`
- **THEN** el sistema la persiste correctamente y la distingue de las facturables
