# Spec Delta

## Purpose

CU-08: La usuaria quiere ver de un vistazo cómo le fue en el mes.

## ADDED Requirements

### Requirement: Resumen mensual

The system SHALL return, for a given month, the total billed, billable and non-billable hours, translated words, active clients and the best client.

#### Scenario: Mes con datos

- **WHEN** hay horas y traducciones en el mes
- **THEN** los totales coinciden con el cálculo mensual y `mejor_cliente` es el de mayor monto

#### Scenario: Mes vacío

- **WHEN** no hay movimientos
- **THEN** `mejor_cliente` es nulo y el total es 0
