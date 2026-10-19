%code requires {
#include "ast.h"
}

%{
#include <stdio.h>
int yylex(void);
void yyerror(const char *s);
int errores = 0;
%}

%code {
Nodo *raiz;
}

%locations
%union { char *str; Nodo *nodo; }

%token TIPO_ENT TIPO_FLOT TIPO_STRING TIPO_CARACTER TIPO_LOGICO
%token WHILE FOR PRINT SI SINO VERDADERO FALSO
%token <str> CADENA NUMERO VARIABLE
%token ASIGNACION NL

%left OR
%left AND
%left IGUAL DIFERENTE
%left MENOR MAYOR MENOR_IGUAL MAYOR_IGUAL
%left SUMA RESTA
%left MULT DIV MOD
%right NOT

%type <nodo> programa linea sentencia tipo expr

%%
programa: /* vacio */      { $$ = raiz = nodo("PROGRAMA", 0); }
        | programa linea   { if ($2) agregar($1, $2); $$ = $1; }
        ;

linea: NL                  { $$ = NULL; }
     | sentencia NL        { $$ = $1; }
     | error NL            { yyerrok; $$ = NULL; }
     ;

sentencia: tipo VARIABLE                      { $$ = nodo("DECLARACION", 2, $1, nodo($2, 0)); }
         | tipo VARIABLE ASIGNACION expr      { $$ = nodo("DECLARACION", 3, $1, nodo($2, 0), $4); }
         | VARIABLE ASIGNACION expr           { $$ = nodo("=", 2, nodo($1, 0), $3); }
         | SI expr                            { $$ = nodo("SI", 1, $2); }
         | SINO                               { $$ = nodo("SINO", 0); }
         | WHILE expr                         { $$ = nodo("MIENTRAS", 1, $2); }
         | FOR VARIABLE ASIGNACION expr expr VARIABLE ASIGNACION expr
                                              { $$ = nodo("PARA", 3, nodo("=", 2, nodo($2, 0), $4), $5,
                                                                     nodo("=", 2, nodo($6, 0), $8)); }
         | PRINT expr                         { $$ = nodo("ESCRIBIR", 1, $2); }
         ;

tipo: TIPO_ENT       { $$ = nodo("ENTERO", 0); }
    | TIPO_FLOT      { $$ = nodo("FLOTANTE", 0); }
    | TIPO_STRING    { $$ = nodo("CADENA", 0); }
    | TIPO_CARACTER  { $$ = nodo("CARACTER", 0); }
    | TIPO_LOGICO    { $$ = nodo("LOGICO", 0); }
    ;

expr: expr OR expr           { $$ = nodo("||", 2, $1, $3); }
    | expr AND expr          { $$ = nodo("&&", 2, $1, $3); }
    | expr IGUAL expr        { $$ = nodo("==", 2, $1, $3); }
    | expr DIFERENTE expr    { $$ = nodo("!=", 2, $1, $3); }
    | expr MENOR expr        { $$ = nodo("<", 2, $1, $3); }
    | expr MAYOR expr        { $$ = nodo(">", 2, $1, $3); }
    | expr MENOR_IGUAL expr  { $$ = nodo("<=", 2, $1, $3); }
    | expr MAYOR_IGUAL expr  { $$ = nodo(">=", 2, $1, $3); }
    | expr SUMA expr         { $$ = nodo("+", 2, $1, $3); }
    | expr RESTA expr        { $$ = nodo("-", 2, $1, $3); }
    | expr MULT expr         { $$ = nodo("*", 2, $1, $3); }
    | expr DIV expr          { $$ = nodo("/", 2, $1, $3); }
    | expr MOD expr          { $$ = nodo("%", 2, $1, $3); }
    | NOT expr               { $$ = nodo("!", 1, $2); }
    | '(' expr ')'           { $$ = $2; }
    | NUMERO                 { $$ = nodo($1, 0); }
    | CADENA                 { $$ = nodo($1, 0); }
    | VARIABLE               { $$ = nodo($1, 0); }
    | VERDADERO              { $$ = nodo("VERDADERO", 0); }
    | FALSO                  { $$ = nodo("FALSO", 0); }
    ;
%%

void yyerror(const char *s) {
    errores++;
    printf("Error sintactico linea %d\n", yylloc.first_line);
}

int main(void) {
    yyparse();
    printf("Se encontraron %d errores\n", errores);

    generar_dot(raiz, "ast.dot");
    return 0;
}
