# Tasks

## 1. Modelo y validación

- [x] 1.1 Crear `app/entities/hora.py` con la entidad `Hora`, el enum `TipoHora` (`facturable` | `planificacion`) y el `CheckConstraint` que exige `minutos > 0`; verificado con `python -c "from app.entities.hora import Hora, TipoHora"` sin errores
- [x] 1.2 Crear `app/dtos/hora_dto.py` con `HoraCreate` y `HoraRead` (`from_attributes=True`); verificado porque el DTO rechaza `minutos` igual a 0, negativo o no entero, y `tipo` fuera del enum

## 2. Persistencia

- [x] 2.1 Crear `app/repositories/hora_repository.py` con `listar`, `obtener_por_id`, `crear` y `eliminar`, pasando `db` como primer argumento y haciendo `commit`/`refresh` dentro; verificado porque el service puede persistir y recuperar un registro

## 3. Reglas de negocio

- [x] 3.1 Crear `app/services/hora_service.py` que lanza 404 si el cliente o la hora no existen, y 422 si el cliente no es de tipo `hora`; verificado con los tests de cliente inexistente, cliente de tipo `palabra` y minutos inválidos en verde

## 4. HTTP

- [x] 4.1 Crear `app/controllers/hora_controller.py` con `GET /api/horas/`, `POST /`, `GET /{id}` y `DELETE /{id}`, usando `Depends(get_db)` y sin lógica de negocio; verificado porque responde 201 al crear, 204 al borrar, 404 y 422 según corresponda
- [x] 4.2 Registrar el router de `horas` en `app/main.py` e importar la entidad en el `lifespan`; verificado porque el servidor arranca y la tabla `horas` se crea en la base

## 5. Pruebas

- [x] 5.1 Crear `tests/test_horas.py` cubriendo el caso feliz y los errores 404 y 422 de la spec; verificado con `pytest tests/test_horas.py` en verde
- [x] 5.2 Correr la suite completa con `pytest` y confirmar que los 27 tests existentes siguen en verde; verificado con la salida real de `pytest`
