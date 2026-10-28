# Design

## Decisions

- **Palabra:** secuencia de letras, números o apóstrofes (`\w+` con soporte de acentos). Los signos de puntuación no cuentan.
- **Repetición exacta:** el texto se divide en segmentos (frases terminadas en `.`, `!`, `?` o líneas). Un segmento es repetido si, ignorando mayúsculas y espacios extra, ya apareció antes. Se cuentan como repetidas las palabras de las apariciones posteriores a la primera.
- **Precio:** se reutiliza `monto_por_palabras` del cálculo mensual, para que el presupuesto y el cobro del mes usen exactamente la misma fórmula.
- **Sin persistencia:** no se crea ninguna fila.
