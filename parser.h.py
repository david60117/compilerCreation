
# Tokens del lenguaje

TIPO_ENT = 258
TIPO_FLOT = 259
TIPO_STRING = 260
TIPO_CARACTER = 261
TIPO_LOGICO = 262

WHILE = 263
FOR = 264
PRINT = 265
SI = 266
SINO = 267

VERDADERO = 268
FALSO = 269
CADENA = 270
NUMERO = 271
VARIABLE = 272
ASIGNACION = 273
NL = 274

OR = 275
AND = 276
IGUAL = 277
DIFERENTE = 278
MENOR = 279
MAYOR = 280
MENOR_IGUAL = 281
MAYOR_IGUAL = 282

SUMA = 283
RESTA = 284
MULT = 285
DIV = 286
MOD = 287
NOT = 288


# Clase para representar un nodo del arbol sintactico
class Nodo:
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho


# Clase para representar los valores del analizador
class YYSTYPE:
    def __init__(self, str_val=None, nodo=None):
        self.str = str_val
        self.nodo = nodo


# Ejemplo de uso
if __name__ == "__main__":
    valor = YYSTYPE(str_val="Hola")
    print("Cadena:", valor.str)

    nodo = Nodo("+", Nodo("5"), Nodo("3"))
    print("Operador:", nodo.valor)
    print("Izquierdo:", nodo.izquierdo.valor)
    print("Derecho:", nodo.derecho.valor)
