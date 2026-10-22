class Nodo:
    def __init__(self, etiqueta, n=0, *hijos):
        self.etiqueta = etiqueta
        self.hijos = list(hijos[:n])
        self.n = len(self.hijos)


def nodo(etiqueta, n=0, *hijos):
    return Nodo(etiqueta, n, *hijos)


def agregar(p, h):
    if p is not None and h is not None:
        p.hijos.append(h)
        p.n = len(p.hijos)
    return p


def generar_dot(raiz, archivo):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("digraph AST {\n")
        f.write("    node [shape=box];\n")

        def recorrer(actual):
            if actual is None:
                return

            f.write(f'    "{id(actual)}" [label="{actual.etiqueta}"];\n')

            for hijo in actual.hijos:
                f.write(f'    "{id(actual)}" -> "{id(hijo)}";\n')
                recorrer(hijo)

        recorrer(raiz)
        f.write("}\n")