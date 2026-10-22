class Nodo:
    def __init__(self, etiqueta):
        self.etiqueta = etiqueta
        self.hijos = []

def agregar(p, h):
    p.hijos.append(h)
    return p

def nodo(etiqueta, *hijos):
    p = Nodo(etiqueta)

    for h in hijos:
        agregar(p, h)

    return p


# Variable para contar los nodos
total_nodos = 0


# Generar los nodos y las conexiones en formato DOT
def dot(archivo, p):
    global total_nodos

    id_nodo = total_nodos
    total_nodos += 1

    # Escribir la etiqueta del nodo
    etiqueta = p.etiqueta.replace("\\", "\\\\").replace('"', '\\"')
    archivo.write(f'  n{id_nodo} [label="{etiqueta}"];\n')

    # Recorrer los hijos
    for h in p.hijos:
        id_hijo = dot(archivo, h)
        archivo.write(f"  n{id_nodo} -> n{id_hijo};\n")

    return id_nodo


# Generar el archivo DOT
def generar_dot(raiz, archivo):
    global total_nodos

    total_nodos = 0

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("digraph AST {\n")
        f.write("  node [shape=box];\n")

        dot(f, raiz)

        f.write("}\n")


# Ejemplo de uso
raiz = nodo(
    "Suma",
    nodo("Numero 5"),
    nodo(
        "Multiplicacion",
        nodo("Numero 3"),
        nodo("Numero 2")
    )
)

generar_dot(raiz, "arbol.dot")

print("Archivo arbol.dot generado correctamente.")