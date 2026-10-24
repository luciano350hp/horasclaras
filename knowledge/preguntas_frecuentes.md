# Preguntas frecuentes

## ¿Para quién es HorasClaras?
Para docentes de inglés y traductores independientes que trabajan con varios clientes y necesitan llevar el control de horas, tarifas y cobros.

## ¿Por qué no me deja registrar horas para un cliente?
Las horas solo se registran en clientes de tipo hora. Si el cliente es por palabra, hay que cargar una traducción.

## ¿Por qué no me deja registrar una traducción?
Las traducciones solo se registran en clientes de tipo palabra y las palabras repetidas no pueden ser más que las totales.

## ¿Por qué no puedo agregar otro cliente?
El límite es de 10 clientes por profesional. Hay que borrar uno para agregar otro.

## ¿Se cobran las horas de planificación?
No. Se registran pero no suman al monto a cobrar.

## ¿Qué pasa si borro un cliente?
Se borran también todas sus horas y traducciones.

## ¿Qué tecnologías usa?
El servidor está hecho con FastAPI, SQLAlchemy y SQLite. Las pantallas con React y Vite. El asistente virtual usa LangChain, Groq y una base de datos vectorial Chroma.

## ¿Puede el asistente ver mis datos o calcular mi cobro?
No. El asistente solo responde sobre cómo funciona la aplicación y sus reglas, usando la documentación. Para ver montos usá "Cobro del mes".
