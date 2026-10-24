# Spec Delta

## Purpose

CU-01: Las profesionales necesitan una cuenta propia para ingresar a la aplicación.

## ADDED Requirements

### Requirement: Registrar una cuenta

The system SHALL allow creating an account with a valid email and a password of at least 6 characters.

#### Scenario: Registro exitoso

- **WHEN** se envían un email válido y una contraseña de 6 o más caracteres
- **THEN** responde 201 sin devolver la contraseña

#### Scenario: Email repetido

- **WHEN** el email ya está registrado
- **THEN** responde 409

#### Scenario: Contraseña corta

- **WHEN** la contraseña tiene menos de 6 caracteres
- **THEN** responde 422

### Requirement: Iniciar sesión

The system SHALL issue a signed access token when the credentials are correct.

#### Scenario: Login correcto

- **WHEN** email y contraseña correctos
- **THEN** responde 200 con un `access_token`

#### Scenario: Credenciales incorrectas

- **WHEN** la contraseña es incorrecta o el email no existe
- **THEN** responde 401

### Requirement: Identificar al usuario

The system SHALL return the current user from a valid token.

#### Scenario: Token válido

- **WHEN** se envía `Authorization: Bearer <token>`
- **THEN** responde 200 con el email del usuario

#### Scenario: Sin token o token falso

- **WHEN** falta el token o no es válido
- **THEN** responde 401
