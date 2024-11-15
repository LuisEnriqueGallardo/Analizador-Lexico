from Analizador import lexer

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0  # Posición del token actual

    def obtener_token(self):
        # Obtiene el token actual sin avanzar el puntero
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def coincidir(self, tipo):
        # Verifica si el token actual coincide con el tipo esperado
        if self.obtener_token() and self.obtener_token().startswith(tipo):
            self.pos += 1  # Avanza si hay coincidencia
            return True
        return False

    def programa(self):
        # Comienza el análisis desde la regla inicial
        if self.coincidir('TOKEN_RESERVADO(BEGIN)'):
            self.instrucciones()
            if not self.coincidir('TOKEN_RESERVADO(END)'):
                raise SyntaxError("Se esperaba 'END'")
        else:
            raise SyntaxError("Se esperaba 'BEGIN' al inicio del programa")

    def instrucciones(self):
        # Procesa una lista de instrucciones hasta llegar al final o encontrar un error
        while self.instruccion():
            print(f"Token después de la instrucción: {self.obtener_token()}")  # Imprime el token actual
            if not self.coincidir('TOKEN_ESPECIAL(;)'):
                raise SyntaxError("Se esperaba ';' después de la instrucción")

    def instruccion(self):
        # Evalúa una instrucción básica y retorna True si es válida
        return self.asignacion() or self.condicional() or self.repeticion()

    def asignacion(self):
        # Asignación básica: ID = Expresión
        if self.coincidir('TOKEN_ID'):
            if not self.coincidir('TOKEN_IGUAL'):
                raise SyntaxError("Se esperaba '=' en la asignación")
            self.expresion()
            return True
        return False

    def condicional(self):
        # Estructura básica de un condicional
        if self.coincidir('TOKEN_RESERVADO(IF)'):
            self.expresion()  # Suponemos que la condición es una expresión simple
            if not self.coincidir('TOKEN_RESERVADO(DO)'):
                raise SyntaxError("Se esperaba 'DO'")
            self.instrucciones()
            if self.coincidir('TOKEN_RESERVADO(ELSE)'):
                self.instrucciones()
            if not self.coincidir('TOKEN_RESERVADO(ENDIF)'):
                raise SyntaxError("Se esperaba 'ENDIF'")
            return True
        return False

    def repeticion(self):
        # Estructura básica de un bucle 'REPEAT ... UNTIL'
        if self.coincidir('TOKEN_RESERVADO(REPEAT)'):
            self.instrucciones()
            if not self.coincidir('TOKEN_RESERVADO(UNTIL)'):
                raise SyntaxError("Se esperaba 'UNTIL'")
            self.expresion()  # Suponemos que la condición es una expresión simple
            return True
        return False

    def expresion(self):
        # Se espera que una expresión básica sea un número o ID, seguido opcionalmente de un operador y otro término
        if self.termino():  # Primero, intenta coincidir con un término básico (ID o NUM)
            # Si después del término hay un operador, continúa la expresión
            while self.coincidir('TOKEN_SUM') or self.coincidir('TOKEN_RES') or \
                self.coincidir('TOKEN_MULT') or self.coincidir('TOKEN_DIV'):
                if not self.termino():
                    raise SyntaxError("Se esperaba un término después del operador en la expresión")
            return True
        else:
            raise SyntaxError("Expresión no válida")

    def termino(self):
        # Un término puede ser un número o un ID
        return self.coincidir('TOKEN_ID') or self.coincidir('TOKEN_NUM')


