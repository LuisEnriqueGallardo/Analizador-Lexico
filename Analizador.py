import re

# Definir las expresiones regulares para los tokens
expresiones_tokens = [
    # Palabras reservadas
    ('TOKEN_RESERVADO', r'\b(BEGIN|END|PROCEDURE|DO|PRINT|AND|OR|NOT|IF|ELSE|ENDIF|REPEAT|UNTIL)\b'),

    # Identificadores (letras mayúsculas)
    ('TOKEN_ID', r'\b[A-Z]+\b'),

    # Constantes numéricas (números enteros)
    ('TOKEN_NUM', r'\b\d+\b'),

    # Constantes de caracteres (entre comillas)
    ('TOKEN_STRING', r'"[^"]*"'),

    # Operadores matemáticos
    ('TOKEN_SUM', r'\+'),  # Operador de suma
    ('TOKEN_RES', r'-'),   # Operador de resta
    ('TOKEN_MULT', r'\*'), # Operador de multiplicación
    ('TOKEN_DIV', r'/'),   # Operador de división

    # Operadores de asignación y comparación
    ('TOKEN_IGUAL', r'='), # Operador de asignación

    # Símbolos especiales
    ('TOKEN_ESPECIAL', r'[",;()#]'),  # Comillas, coma, punto y coma, paréntesis, almohadilla

    # Espacios en blanco (se ignoran)
    ('TOKEN_SKIP', r'[ \t]+'),

    # Nueva línea para facilitar el seguimiento de línea
    ('TOKEN_NL', r'\n'),

    # Secuencia de caracteres no reconocidos (error)
    ('TOKEN_ERR', r'[^\s]+'),

    # Cualquier otro carácter no reconocido
    ('TOKEN_DESCONOCIDO', r'.'),
]


# Crear una expresión regular para reconocer los tokens
token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in expresiones_tokens)
token_re = re.compile(token_re)


def lexer(texto):
    """Función que realiza el análisis léxico de un texto de entrada.

    Args:
        texto (str): Texto de entrada a analizar.

    Returns:
        tokens: Lista de tokens reconocidos.
    """
    tokens = []
    tokensERR = []
    tokensOriginales = []
    tokensOriginalesERR = []
    numeroDeLinea = 1
    for mo in token_re.finditer(texto):
        tipo = mo.lastgroup
        value = mo.group()
        if tipo == 'TOKEN_NL':
            numeroDeLinea += 1
        elif tipo == 'TOKEN_SKIP':
            continue
        elif tipo == 'TOKEN_ERR':
            tokensERR.append(f"Linea {numeroDeLinea}: Cadena no reconocido ({value})")
            tokensOriginalesERR.append(f"{tipo}({value})")
        elif tipo == 'TOKEN_DESCONOCIDO':
            tokensERR.append(f"Linea {numeroDeLinea}: Caracter desconocido ({value})")      
            tokensOriginalesERR.append(f"{tipo}({value})")
        else:
            tokens.append(f"Linea {numeroDeLinea}: {tipo}({value})")
            tokensOriginales.append(f"{tipo}({value})")
    return tokens, tokensERR, tokensOriginales, tokensOriginalesERR