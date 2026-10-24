# Reglas de negocio de HorasClaras

## Tipos de cliente
Un cliente puede ser de tipo **hora** (se le cobra por hora trabajada) o de tipo **palabra** (se le cobra por palabra traducida). El tipo se elige al crear el cliente y define qué se puede registrar: horas para los clientes por hora, traducciones para los clientes por palabra.

## Límite de clientes
Cada profesional puede tener como máximo **10 clientes**. Al intentar crear el cliente número 11 la aplicación lo rechaza con un error de conflicto.

## Cálculo del monto por hora
El monto de un cliente por hora es: minutos facturables dividido 60, multiplicado por la tarifa por hora. Por ejemplo, 120 minutos facturables con una tarifa de 30 por hora dan 60.

## Horas no facturables (planificación)
Las horas de tipo **planificación** (preparar clases, organizar material) se registran para llevar el control del tiempo pero **nunca se cobran**: no suman al monto del mes. Sí aparecen en el dashboard como horas no facturables.

## Cálculo del monto por palabra
Las palabras nuevas se cobran a tarifa completa. Las palabras **repetidas** (que ya se tradujeron antes) se cobran con descuento. Fórmula: (palabras totales menos repetidas) por tarifa, más repetidas por tarifa por (1 menos descuento/100).
Ejemplo: 1000 palabras totales, 400 repetidas, tarifa 0,10 y descuento 50%: 600 por 0,10 = 60, más 400 por 0,10 por 0,5 = 20. Total 80.

## Descuento por repetición
El descuento por repetición es un porcentaje entre 0 y 100. Si no se indica, vale **50%**. Solo se aplica a las palabras repetidas, nunca a las nuevas.

## Palabras repetidas
Las palabras repetidas no pueden superar a las palabras totales del trabajo.

## Cálculo mensual
El cobro se calcula por mes, con formato año-mes (por ejemplo 2026-05). Se calcula por cliente y se suma el total del mes. Un mes sin movimientos da 0.
