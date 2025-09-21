Proyecto Compilador: Analizador Léxico-Sintáctico LR
Este repositorio contiene el avance de un proyecto para la materia de Compiladores. El objetivo es desarrollar un analizador léxico y sintáctico completo, capaz de validar la estructura de un lenguaje de programación específico.

🚧 Estado Actual: Proyecto en Desarrollo 🚧
La fase actual del proyecto se centra en el análisis sintáctico. El motor del parser LR es funcional y se ha integrado con una interfaz gráfica para la visualización del proceso. El analizador es genérico, lo que significa que puede operar con diferentes gramáticas siempre que se le proporcione el archivo de tablas correspondiente.

✨ Características Principales
Analizador Léxico (Lexer): Capaz de tokenizar palabras reservadas, identificadores, números (enteros y flotantes), cadenas y operadores de un lenguaje similar a C.

Motor de Parser LR Genérico: No tiene una gramática fija en el código. Lee la gramática y las tablas de acción/GOTO desde un archivo compilador.lr externo.

Visualización Animada: Incluye una interfaz gráfica (GUI) construida con Tkinter que muestra el proceso de análisis (Pila, Entrada, Salida) paso a paso, facilitando la depuración y el entendimiento del algoritmo.

Manejo de Errores: El parser es capaz de detectar y reportar errores de sintaxis cuando una secuencia de tokens no es válida según la gramática, y también detecta inconsistencias en la tabla LR proporcionada.

💻 Tecnologías Utilizadas
Python 3

Tkinter: Para la construcción de la interfaz gráfica de usuario.

Módulo re: Para el análisis léxico basado en expresiones regulares.

