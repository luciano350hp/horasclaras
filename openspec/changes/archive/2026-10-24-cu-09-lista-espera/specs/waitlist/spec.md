# Spec Delta

## Purpose

CU-09: Captar emails de personas interesadas antes del lanzamiento.

## ADDED Requirements

### Requirement: Anotarse en la lista de espera

The system SHALL register an email in the waiting list, normalized to lowercase.

#### Scenario: Alta exitosa

- **WHEN** se envía un email válido
- **THEN** responde 201 con el email en minúsculas

#### Scenario: Formato inválido

- **WHEN** el email no tiene formato válido
- **THEN** responde 422

#### Scenario: Email repetido

- **WHEN** el email ya está en la lista (aunque cambien mayúsculas)
- **THEN** responde 409

### Requirement: Listar la lista de espera

The system SHALL list registered emails.

#### Scenario: Listado

- **WHEN** hay emails anotados
- **THEN** responde 200 con todos
