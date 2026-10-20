---
name: reglas-tarifas
description: Use when calculating amounts to bill, counting words, or handling billable vs planning hours in HorasClaras.
---

# Reglas de negocio de tarifas (fuente: propuesta del TP)

- Cliente tipo `hora`: monto = (minutos facturables / 60) x tarifa. Las horas de `planificacion` NUNCA se cobran, pero se muestran en columna aparte.
- Cliente tipo `palabra`: monto = (palabras totales - repetidas) x tarifa + repetidas x tarifa x (1 - descuento/100).
- `descuento_repeticion`: porcentaje 0..100, por cliente, por defecto 50. Se aplica solo a las palabras repetidas, no al total.
- Las palabras repetidas no pueden superar las totales.
- Maximo 10 clientes. La tarifa debe ser mayor a 0.
- Registro de horas: solo para clientes `hora`; duracion en minutos (entero > 0); cliente y fecha obligatorios.
- Los calculos se hacen por cliente y por mes (formato YYYY-MM). Usar `Decimal`, nunca float.
- No se guardan facturas: el tarifario PDF se calcula al momento y solo si el mes tiene registros.