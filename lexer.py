
import re

linea = 1

palabras = {
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
    "FALSO": "FALSO"
}

operadores = {
    "==": "IGUAL",
    "!=": "DIFERENTE",
    "<=": "MENOR_IGUAL",
    ">=": "MAYOR_IGUAL",
    "<": "MENOR",
    ">": "MAYOR",
    "&&": "AND",
    "||": "OR",
    "!": "NOT",
    "=": "ASIGNACION",
    "+": "SUMA",
    "-": "RESTA",
    "*": "MULT",
    "/": "DIV",
    "%": "MOD"
}

patron = re.compile(
    r'"[^"\n]*"|'
    r'[0-9]+(?:\.[0-9]+)?|'
    r'[a-zA-Z_][a-zA-Z0-9_]*|'
    r'==|!=|<=|>=|&&|\|\||[<>!=+\-*/%=]|'
    r'\n|[ \t\r]+|.'
)

def analizar(codigo):
    global linea

    linea = 1
    tokens = []

    for coincidencia in patron.finditer(codigo):
        texto = coincidencia.group()

        if texto in (" ", "\t", "\r") or texto.isspace() and texto != "\n":
            continue

        if texto == "\n":
            tokens.append(("NL", texto, linea))
            linea += 1

        elif texto in palabras:
            tokens.append((palabras[texto], texto, linea))

        elif texto.startswith('"') and texto.endswith('"'):
            tokens.append(("CADENA", texto, linea))

        elif re.fullmatch(r'[0-9]+(?:\.[0-9]+)?', texto):
            tokens.append(("NUMERO", texto, linea))

        elif re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', texto):
            tokens.append(("VARIABLE", texto, linea))

        elif texto in operadores:
            tokens.append((operadores[texto], texto, linea))

        else:
            tokens.append((texto, texto, linea))

    if not tokens or tokens[-1][0] != "NL":
        tokens.append(("NL", "\\n", linea))

    return tokens


# Programa principal
codigo = input("Escribe el codigo a analizar: ")

resultado = analizar(codigo)

print("\nTokens encontrados:")
for tipo, valor, num_linea in resultado:
    print(f"Linea {num_linea}: {tipo} -> {valor}")
