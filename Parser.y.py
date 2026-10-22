
import re

errores = 0
raiz = None


class Nodo:
    def __init__(self, valor, hijos=None):
        self.valor = valor
        self.hijos = hijos if hijos else []


def nodo(valor, *hijos):
    return Nodo(valor, list(hijos))


def agregar(padre, hijo):
    if hijo:
        padre.hijos.append(hijo)


def analizar_expr(expresion):
    expresion = expresion.strip()

    if not expresion:
        return None

    # Quitar parentesis externos
    if expresion.startswith("(") and expresion.endswith(")"):
        return analizar_expr(expresion[1:-1])

    # Buscar operadores
    operadores = [
        ("||", "||"), ("&&", "&&"),
        ("==", "=="), ("!=", "!="),
        ("<=", "<="), (">=", ">="),
        ("<", "<"), (">", ">"),
        ("+", "+"), ("-", "-"),
        ("*", "*"), ("/", "/"), ("%", "%")
    ]

    for operador, nombre in operadores:
        partes = expresion.split(operador, 1)

        if len(partes) == 2 and partes[0].strip() and partes[1].strip():
            izquierda = analizar_expr(partes[0])
            derecha = analizar_expr(partes[1])

            return nodo(nombre, izquierda, derecha)

    if expresion.startswith("!"):
        return nodo("!", analizar_expr(expresion[1:]))

    if expresion == "VERDADERO":
        return nodo("VERDADERO")

    if expresion == "FALSO":
        return nodo("FALSO")

    if expresion.startswith('"') and expresion.endswith('"'):
        return nodo(expresion)

    return nodo(expresion)


def analizar_linea(linea):
    linea = linea.strip()

    if not linea:
        return None

    # Declaraciones de variables
    tipos = {
        "entero": "ENTERO",
        "flotante": "FLOTANTE",
        "string": "CADENA",
        "caracter": "CARACTER",
        "logico": "LOGICO"
    }

    patron = r'^(entero|flotante|string|caracter|logico)\s+([a-zA-Z_]\w*)(?:\s*=\s*(.+))?$'
    coincidencia = re.match(patron, linea, re.IGNORECASE)

    if coincidencia:
        tipo = tipos[coincidencia.group(1).lower()]
        variable = coincidencia.group(2)
        valor = coincidencia.group(3)

        if valor:
            return nodo(
                "DECLARACION",
                nodo(tipo),
                nodo(variable),
                analizar_expr(valor)
            )

        return nodo("DECLARACION", nodo(tipo), nodo(variable))

    # Asignacion
    coincidencia = re.match(r'^([a-zA-Z_]\w*)\s*=\s*(.+)$', linea)

    if coincidencia:
        variable = coincidencia.group(1)
        expresion = coincidencia.group(2)

        return nodo(
            "=",
            nodo(variable),
            analizar_expr(expresion)
        )

    # Condiciones
    if linea.startswith("si "):
        return nodo("SI", analizar_expr(linea[3:]))

    if linea == "sino":
        return nodo("SINO")

    # Ciclo while
    if linea.startswith("while "):
        return nodo("MIENTRAS", analizar_expr(linea[6:]))

    # Imprimir
    if linea.startswith("print "):
        return nodo("ESCRIBIR", analizar_expr(linea[6:]))

    return None


def generar_dot(arbol, archivo):
    lineas = ["digraph AST {", 'node [shape=box];']
    contador = 0

    def recorrer(actual):
        nonlocal contador

        if actual is None:
            return

        mi_id = contador
        contador += 1

        etiqueta = actual.valor.replace('"', '\\"')
        lineas.append(f'n{mi_id} [label="{etiqueta}"];')

        for hijo in actual.hijos:
            if hijo is not None:
                hijo_id = recorrer(hijo)
                lineas.append(f"n{mi_id} -> n{hijo_id};")

        return mi_id

    recorrer(arbol)
    lineas.append("}")

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))


def main():
    global raiz, errores

    raiz = nodo("PROGRAMA")

    print("Escribe tu codigo (escribe FIN para terminar):")

    while True:
        linea = input("> ")

        if linea.strip().upper() == "FIN":
            break

        resultado = analizar_linea(linea)

        if resultado:
            agregar(raiz, resultado)
        elif linea.strip():
            errores += 1
            print("Error sintactico:", linea)

    print("Se encontraron", errores, "errores")

    generar_dot(raiz, "ast.dot")
    print("Se genero el archivo ast.dot")


if __name__ == "__main__":
    main()
