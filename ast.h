#ifndef AST_H
#define AST_H

#include <stdio.h>

typedef struct Nodo {
    char *etiqueta;
    struct Nodo **hijos;
    int n;
} Nodo;

Nodo *nodo(const char *etiqueta, int n, ...);
Nodo *agregar(Nodo *p, Nodo *h);
void generar_dot(Nodo *raiz, const char *archivo);

#endif
