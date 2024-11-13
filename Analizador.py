import re

# Definir los patrones de tokens basados en las especificaciones
expresiones_tokens = [
    ('TOKEN_RESERVADO',   r'\b(BEGIN|END|PROCEDURE|DO|PRINT|AND|OR|NOT|IF|ELSE|ENDIF|REPEAT|UNTIL)\b'),  # Palabras reservadas
    ('TOKEN_ID',         r'\b[A-Z]+\b'),           # Identificadores (letras mayúsculas)
    ('TOKEN_NUM',     r'\b\d+\b'),              # Constantes numéricas (números enteros)
    ('TOKEN_STRING',     r'"[^"]*"'),              # Constantes de caracteres (entre comillas)
    ('TOKEN_SUM',       r'\+'),                   # Operador +
    ('TOKEN_RES',      r'-'),                    # Operador -
    ('TOKEN_MULT',       r'\*'),                   # Operador *
    ('TOKEN_DIV',        r'/'),                    # Operador /
    ('TOKEN_IGUAL',     r'='),                    # Operador =
    ('TOKEN_ESPECIAL',    r'[",;()#]'),             # Símbolos especiales (" , ; ( ) #)
    ('TOKEN_SKIP',       r'[ \t]+'),               # Espacios en blanco (se ignoran)
    ('TOKEN_NL',    r'\n'),                   # Nueva línea para facilitar el seguimiento de línea
    ('TOKEN_ERR',       r'[^\s]+'),               # Secuencia de caracteres no reconocidos (error)
    ('TOKEN_DESCONOCIDO', r'.'),  # Cualquier otro carácter no reconocido
]

# Compilar la expresión regular
token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in expresiones_tokens)
token_re = re.compile(token_re)

# Lexer para analizar el código fuente
def lexer(texto):
    tokens = []
    tokensERR = []
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
        elif tipo == 'TOKEN_DESCONOCIDO':
            tokensERR.append(f"Linea {numeroDeLinea}: Caracter desconocido ({value})")        
        else:
            tokens.append(f"Linea {numeroDeLinea}: {tipo}({value})")
    return tokens, tokensERR