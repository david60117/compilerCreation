%{
#include <stdio.h>
int yylex(void);
void yyerror(const char *s);
int errores = 0;
%}

%locations
%union { const char *msg; }

%token TIPO_ENT TIPO_FLOT TIPO_STRING TIPO_CARACTER TIPO_LOGICO
%token WHILE FOR PRINT SI SINO VERDADERO FALSO
%token CADENA NUMERO VARIABLE ASIGNACION NL

%left OR
%left AND
%left IGUAL DIFERENTE
%left MENOR MAYOR MENOR_IGUAL MAYOR_IGUAL
%left SUMA RESTA
%left MULT DIV MOD
%right NOT

%type <msg> sentencia

%%
programa: /* vacio */
        | programa linea
        ;

linea: NL
     | sentencia NL
     | error NL         { yyerrok; }
     ;

sentencia: tipo VARIABLE                      { $$ = "declaracion correcta"; }
         | tipo VARIABLE ASIGNACION expr      { $$ = "declaracion correcta"; }
         | VARIABLE ASIGNACION expr           { $$ = "asignacion correcta"; }
         | SI expr                            { $$ = "condicion SI correcta"; }
         | SINO                               { $$ = "SINO correcto"; }
         | WHILE expr                         { $$ = "ciclo MIENTRAS correcto"; }
         | FOR VARIABLE ASIGNACION expr expr VARIABLE ASIGNACION expr
                                              { $$ = "ciclo PARA correcto"; }
         | PRINT expr                         { $$ = "escritura correcta"; }
         ;

tipo: TIPO_ENT | TIPO_FLOT | TIPO_STRING | TIPO_CARACTER | TIPO_LOGICO ;

expr: expr OR expr
    | expr AND expr
    | expr IGUAL expr
    | expr DIFERENTE expr
    | expr MENOR expr
    | expr MAYOR expr
    | expr MENOR_IGUAL expr
    | expr MAYOR_IGUAL expr
    | expr SUMA expr
    | expr RESTA expr
    | expr MULT expr
    | expr DIV expr
    | expr MOD expr
    | NOT expr
    | '(' expr ')'
    | NUMERO
    | CADENA
    | VARIABLE
    | VERDADERO
    | FALSO
    ;
%%

void yyerror(const char *s) {
    errores++;
    printf("Error sintactico linea %d\n", yylloc.first_line);
}

int main(void) {
    yyparse();
    printf("Se encontraron %d errores\n", errores);
    return 0;
}
