#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include "ast.h"

Nodo *agregar(Nodo *p, Nodo *h) {
    p->hijos = realloc(p->hijos, (p->n + 1) * sizeof(Nodo *));
    p->hijos[p->n++] = h;
    return p;
}

Nodo *nodo(const char *etiqueta, int n, ...) {
    Nodo *p = calloc(1, sizeof(Nodo));
    p->etiqueta = strdup(etiqueta);
    va_list ap;
    va_start(ap, n);
    for (int i = 0; i < n; i++) agregar(p, va_arg(ap, Nodo *));
    va_end(ap);
    return p;
}

static int total_nodos = 0;

static int dot(FILE *f, Nodo *p) {
    int id = total_nodos++;
    fprintf(f, "  n%d [label=\"", id);
    for (char *c = p->etiqueta; *c; c++) {
        if (*c == '"' || *c == '\\') fputc('\\', f);
        fputc(*c, f);
    }
    fprintf(f, "\"];\n");
    for (int i = 0; i < p->n; i++) {
        int h = dot(f, p->hijos[i]);
        fprintf(f, "  n%d -> n%d;\n", id, h);
    }
    return id;
}

void generar_dot(Nodo *raiz, const char *archivo) {
    FILE *f = fopen(archivo, "w");
    fprintf(f, "digraph AST {\n  node [shape=box];\n");
    dot(f, raiz);
    fprintf(f, "}\n");
    fclose(f);
}
