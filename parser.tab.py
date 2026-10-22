import re

# Analizador sintactico en Python basado en las reglas del archivo de Bison.

PALABRAS = {
    "ENTERO": "TIPO_ENT",
    "FLOTANTE": "TIPO_FLOT",
    "CADENA": "TIPO_STRING",
    "CARACTER": "TIPO_CARACTER",
    "LOGICO": "TIPO_LOGICO",
    "MIENTRAS": "WHILE",
    "PARA": "FOR",
    "ESCRIBIR": "PRINT",
    "SI": "SI",
    "SINO": "SINO",
    "VERDADERO": "VERDADERO",
    "FALSO": "FALSO",
}

OPERADORES = {
    "||": "OR", "&&": "AND",
    "==": "IGUAL", "!=": "DIFERENTE",
    "<=": "MENOR_IGUAL", ">=": "MAYOR_IGUAL",
    "<": "MENOR", ">": "MAYOR",
    "!": "NOT", "=": "ASIGNACION",
    "+": "SUMA", "-": "RESTA", "*": "MULT",
    "/": "DIV", "%": "MOD",
}

PATRON = re.compile(
    r'"[^"\n]*"|'
    r'[0-9]+(?:\.[0-9]+)?|'
    r'[a-zA-Z_][a-zA-Z0-9_]*|'
    r'==|!=|<=|>=|&&|\|\||[()<>!=+\-*/%=]|\n|[ \t\r]+|.'
)

class ErrorSintaxis(Exception):
    pass


class Nodo:
    def __init__(self, valor, hijos=None):
        self.valor = valor
        self.hijos = hijos or []

    def mostrar(self, nivel=0):
        print("  " * nivel + str(self.valor))
        for hijo in self.hijos:
            hijo.mostrar(nivel + 1)


def crear_nodo(valor, *hijos):
    return Nodo(valor, list(hijos))


def analizar_lexico(codigo):
    tokens = []
    linea = 1

    for coincidencia in PATRON.finditer(codigo):
        texto = coincidencia.group()

        if texto.isspace() and texto != "\n":
            continue

        if texto == "\n":
            tokens.append(("NL", texto, linea))
            linea += 1
        elif texto.startswith('"') and texto.endswith('"'):
            tokens.append(("CADENA", texto, linea))
        elif re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', texto):
            tokens.append(("NUMERO", texto, linea))
        elif re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', texto):
            tokens.append((PALABRAS.get(texto, "VARIABLE"), texto, linea))
        elif texto in OPERADORES:
            tokens.append((OPERADORES[texto], texto, linea))
        elif texto in ("(", ")"):
            tokens.append((texto, texto, linea))
        else:
            raise ErrorSintaxis(f"Caracter no reconocido '{texto}' en la linea {linea}")

    if not tokens or tokens[-1][0] != "NL":
        tokens.append(("NL", "\\n", linea))
    tokens.append(("EOF", "", linea))
    return tokens


class Analizador:
    # De menor a mayor prioridad, siguiendo los operadores del lenguaje.
    PRECEDENCIA = {
        "OR": 1,
        "AND": 2,
        "IGUAL": 3, "DIFERENTE": 3,
        "MENOR": 4, "MAYOR": 4, "MENOR_IGUAL": 4, "MAYOR_IGUAL": 4,
        "SUMA": 5, "RESTA": 5,
        "MULT": 6, "DIV": 6, "MOD": 6,
    }

    TIPOS = {
        "TIPO_ENT": "ENTERO",
        "TIPO_FLOT": "FLOTANTE",
        "TIPO_STRING": "CADENA",
        "TIPO_CARACTER": "CARACTER",
        "TIPO_LOGICO": "LOGICO",
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def actual(self):
        return self.tokens[self.pos]

    def aceptar(self, tipo):
        if self.actual()[0] == tipo:
            token = self.actual()
            self.pos += 1
            return token
        return None

    def exigir(self, tipo):
        token = self.aceptar(tipo)
        if token is None:
            actual = self.actual()
            raise ErrorSintaxis(
                f"Se esperaba {tipo}, pero se encontro '{actual[1]}' "
                f"en la linea {actual[2]}"
            )
        return token

    def analizar(self):
        raiz = crear_nodo("PROGRAMA")
        while self.actual()[0] != "EOF":
            if self.aceptar("NL"):
                continue
            linea = self.actual()[2]
            try:
                sentencia = self.sentencia()
                self.exigir("NL")
                raiz.hijos.append(sentencia)
            except ErrorSintaxis:
                # Recuperacion: avanzar hasta el siguiente salto de linea.
                while self.actual()[0] not in ("NL", "EOF"):
                    self.pos += 1
                self.aceptar("NL")
                raise
        return raiz

    def sentencia(self):
        tipo = self.actual()[0]

        if tipo in self.TIPOS:
            tipo_nodo = crear_nodo(self.TIPOS[self.exigir(tipo)[0]])
            nombre = self.exigir("VARIABLE")[1]
            variable = crear_nodo(nombre)
            if self.aceptar("ASIGNACION"):
                valor = self.expresion()
                return crear_nodo("DECLARACION", tipo_nodo, variable, valor)
            return crear_nodo("DECLARACION", tipo_nodo, variable)

        if tipo == "VARIABLE":
            nombre = self.exigir("VARIABLE")[1]
            self.exigir("ASIGNACION")
            return crear_nodo("=", crear_nodo(nombre), self.expresion())

        if self.aceptar("SI"):
            return crear_nodo("SI", self.expresion())

        if self.aceptar("SINO"):
            return crear_nodo("SINO")

        if self.aceptar("WHILE"):
            return crear_nodo("MIENTRAS", self.expresion())

        if self.aceptar("FOR"):
            nombre_inicio = self.exigir("VARIABLE")[1]
            self.exigir("ASIGNACION")
            inicio = self.expresion()
            condicion = self.expresion()
            nombre_paso = self.exigir("VARIABLE")[1]
            self.exigir("ASIGNACION")
            paso = self.expresion()
            asignacion_inicio = crear_nodo("=", crear_nodo(nombre_inicio), inicio)
            asignacion_paso = crear_nodo("=", crear_nodo(nombre_paso), paso)
            return crear_nodo("PARA", asignacion_inicio, condicion, asignacion_paso)

        if self.aceptar("PRINT"):
            return crear_nodo("ESCRIBIR", self.expresion())

        actual = self.actual()
        raise ErrorSintaxis(
            f"Sentencia no valida cerca de '{actual[1]}' en la linea {actual[2]}"
        )

    def expresion(self, minimo=1):
        token = self.actual()

        if self.aceptar("NOT"):
            izquierda = crear_nodo("!", self.expresion(7))
        elif self.aceptar("("):
            izquierda = self.expresion()
            self.exigir(")")
        elif token[0] in ("NUMERO", "CADENA", "VARIABLE", "VERDADERO", "FALSO"):
            self.pos += 1
            izquierda = crear_nodo(token[1])
        else:
            raise ErrorSintaxis(
                f"Expresion no valida cerca de '{token[1]}' en la linea {token[2]}"
            )

        while True:
            tipo = self.actual()[0]
            prioridad = self.PRECEDENCIA.get(tipo, 0)
            if prioridad < minimo:
                break
            operador = self.actual()[1]
            self.pos += 1
            derecha = self.expresion(prioridad + 1)
            izquierda = crear_nodo(operador, izquierda, derecha)

        return izquierda


def analizar(codigo):
    tokens = analizar_lexico(codigo)
    return Analizador(tokens).analizar()


if __name__ == "__main__":
    print("Analizador sintactico")
    print("Escribe el codigo. Deja una linea vacia para terminar:")
    lineas = []
    while True:
        try:
            linea = input()
        except EOFError:
            break
        if linea == "":
            break
        lineas.append(linea)

    codigo = "\n".join(lineas)

    try:
        arbol = analizar(codigo)
        print("\nCodigo correcto. Arbol sintactico:")
        arbol.mostrar()
    except ErrorSintaxis as error:
        print("\nError de sintaxis:", error)
