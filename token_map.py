# token_map.py
# Este archivo es CRUCIAL. Mapea los nombres de los tokens a su número de columna
# en la tabla del archivo .lr. He hecho una suposición basada en un orden común,
# pero DEBES VERIFICAR Y CORREGIR estos valores según la especificación de tu proyecto.

# El ID 23 suele ser el fin de archivo ($)
TOKEN_EOF_ID = 23

# Mapa de palabras reservadas y símbolos a sus IDs de token (columnas)
TOKEN_MAP = {
    # Palabras Reservadas
    'if': 18,
    'else': 22,
    'while': 19,
    'return': 20,
    'int': 4,
    'float': 4,
    'void': 4,
    
    # Símbolos y Operadores
    ';': 12,
    ',': 13,
    '(': 14,
    ')': 15,
    '{': 16,
    '}': 17,
    '=': 8,
    '+': 5,
    '-': 5,
    '*': 6,
    '/': 6,
    '<': 7,
    '>': 7,
    '<=': 7,
    '>=': 7,
    '==': 10,
    '!=': 10,
    '&&': 11,
    '||': 9,
    
    # Tipos de Token Genéricos
    'id': 0,
    'entero': 2,
    'flotante': 3,
    'cadena': 1, # Asumiendo que 'cadena' es el token 1
}

# Nombres de los símbolos no-terminales (para imprimir la regla de reducción)
# El ID de un no-terminal es su número de regla (24-45)
NON_TERMINAL_MAP = {
    24: 'programa', 25: 'Definiciones', 26: 'Definicion', 27: 'DefVar',
    28: 'ListaVar', 29: 'DefFunc', 30: 'Parametros', 31: 'ListaParam',
    32: 'BloqFunc', 33: 'DefLocales', 34: 'DefLocal', 35: 'Sentencias',
    36: 'Sentencia', 37: 'Otro', 38: 'Bloque', 39: 'ValorRegresa',
    40: 'Argumentos', 41: 'ListaArgumentos', 42: 'Termino', 43: 'LlamadaFunc',
    44: 'SentenciaBloque', 45: 'Expresion'
}