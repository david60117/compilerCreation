import re

# Analizador lexico en Python equivalente a las reglas identificadas
# en el archivo generado por Flex.

PALABRAS_RESERVADAS = {
    "int": "TIPO_ENT",
    "float": "TIPO_FLOT",
    "string": "TIPO_STRING",
    "char": "TIPO_CARACTER",
    "bool": "TIPO_LOGICO",
    "while": "WHILE",
    "for": "FOR",
    "print": "PRINT",
    "if": "SI",
    "else": "SINO",
    "true": "VERDADERO",
    "false": "FALSO",
}

# Los patrones se revisan en orden: los operadores de dos caracteres
# deben reconocerse antes que los de un solo carácter.
PATRONES = [
    ("ESPACIOS", r"[ \t\r]+"),
    ("NL", r"\n"),
    ("COMENTARIO", r"//[^\n]*"),
    ("CADENA", r'"(?:\\.|[^"\\])*"'),
    ("CARACTER", r"'(?:\\.|[^'\\])'"),
    ("NUMERO", r"\d+(?:\.\d+)?"),
    ("VARIABLE", r"[A-Za-z_][A-Za-z0-9_]*"),
    ("IGUAL", r"=="),
    ("DIFERENTE", r"!="),
    ("MENOR_IGUAL", r"<="),
    ("MAYOR_IGUAL", r">="),
    ("AND", r"&&"),
    ("OR", r"\|\|"),
    ("NOT", r"!"),
    ("ASIGNACION", r"="),
    ("SUMA", r"\+"),
    ("RESTA", r"-"),
    ("MULT", r"\*"),
    ("DIV", r"/"),
    ("MOD", r"%"),
    ("MENOR", r"<"),
    ("MAYOR", r">"),
    ("SIMBOLO", r"[(){}\[\];,]"),
]

def analizar(codigo):
    tokens = []
    linea = 1
    posicion = 0

    while posicion < len(codigo):
        encontrado = False

        for tipo, patron in PATRONES:
            coincidencia = re.match(patron, codigo[posicion:])
            if coincidencia:
                texto = coincidencia.group(0)
                encontrado = True

                if tipo == "NL":
                    tokens.append(("NL", "\\n", linea))
                    linea += 1
                elif tipo not in ("ESPACIOS", "COMENTARIO"):
                    if tipo == "VARIABLE":
                        tipo = PALABRAS_RESERVADAS.get(texto, "VARIABLE")
                    tokens.append((tipo, texto, linea))

                posicion += len(texto)
                break

        if not encontrado:
            # Mantiene el comportamiento de devolver el carácter
            # cuando no coincide con una regla específica.
            caracter = codigo[posicion]
            tokens.append(("CARACTER_DESCONOCIDO", caracter, linea))
            posicion += 1

    if not tokens or tokens[-1][0] != "NL":
        tokens.append(("NL", "\\n", linea))

    return tokens

def main():
    print("Analizador lexico")
    print("Escribe el codigo que quieres analizar.")
    print("Escribe FIN en una linea para terminar la entrada.\\n")

    lineas = []
    while True:
        try:
            linea = input()
        except EOFError:
            break
        if linea.strip() == "FIN":
            break
        lineas.append(linea)

    codigo = "\\n".join(lineas)
    resultado = analizar(codigo)

    print("\\nTOKENS ENCONTRADOS:")
    for tipo, valor, numero_linea in resultado:
        print(f"Linea {numero_linea}: {tipo} -> {valor}")

if __name__ == "__main__":
    main()
