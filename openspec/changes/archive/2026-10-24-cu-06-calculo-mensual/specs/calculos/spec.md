# Spec Delta

## Purpose

CU-05 y CU-06: El objetivo del producto es saber cuánto cobrar a cada cliente cada mes, sin cuentas a mano. CU-05 (horas no facturables) se resuelve acá: se registran pero no suman al monto.

## ADDED Requirements

### Requirement: Calcular el monto del mes

The system SHALL compute, for each client and a given month, the amount to charge; hour clients by billable minutes and word clients by total and repeated words.

#### Scenario: Cálculo combinado

- **WHEN** hay horas facturables, horas de planificación y traducciones en el mes
- **THEN** el monto de hora solo suma las facturables y el de palabra aplica el descuento a las repetidas; se devuelve el total

#### Scenario: Mes sin datos

- **WHEN** no hay movimientos en el mes
- **THEN** los montos y el total son 0

#### Scenario: Filtro por cliente

- **WHEN** se pasa `cliente_id`
- **THEN** se devuelve solo ese cliente

#### Scenario: Cliente inexistente

- **WHEN** el `cliente_id` no existe
- **THEN** responde 404

#### Scenario: Mes inválido

- **WHEN** el mes no tiene formato `YYYY-MM`
- **THEN** responde 422

### Requirement: Horas no facturables

The system MUST NOT include planning hours in the amount to charge, and SHALL report them separately.

#### Scenario: Planificación informada

- **WHEN** un cliente por hora tiene minutos de planificación
- **THEN** aparecen en `minutos_no_facturables` y no suman al monto
