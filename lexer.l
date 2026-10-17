%{
#include <stdio.h>
%}
%option noyywrap

%%
ENTERO                            { fprintf(yyout, "TIPO_ENT "); }
FLOTANTE                          { fprintf(yyout, "TIPO_FLOT "); }
CADENA                            { fprintf(yyout, "TIPO_STRING "); }
CARACTER                          { fprintf(yyout, "TIPO_CARACTER "); }
LOGICO                            { fprintf(yyout, "TIPO_LOGICO "); }
MIENTRAS                          { fprintf(yyout, "WHILE "); }
PARA                              { fprintf(yyout, "FOR "); }
ESCRIBIR                          { fprintf(yyout, "PRINT "); }

SI                                { fprintf(yyout, "SI "); }
SINO                              { fprintf(yyout, "SINO "); }

VERDADERO                         { fprintf(yyout, "VERDADERO "); }
FALSO                             { fprintf(yyout, "FALSO "); }

["][^"]*["]                       { fprintf(yyout, "CADENA "); }
[0-9]+([.][0-9]+)?                { fprintf(yyout, "NUMERO "); }
[a-zA-Z_][a-zA-Z0-9_]*            { fprintf(yyout, "VARIABLE "); }

"=="                              { fprintf(yyout, "IGUAL "); }
"!="                              { fprintf(yyout, "DIFERENTE "); }
"<="                              { fprintf(yyout, "MENOR_IGUAL "); }
">="                              { fprintf(yyout, "MAYOR_IGUAL "); }
"<"                               { fprintf(yyout, "MENOR "); }
">"                               { fprintf(yyout, "MAYOR "); }

"&&"                              { fprintf(yyout, "AND "); }
"||"                              { fprintf(yyout, "OR "); }
"!"                               { fprintf(yyout, "NOT "); }

"="                               { fprintf(yyout, "ASIGNACION "); }

"+"                               { fprintf(yyout, "SUMA "); }
"-"                               { fprintf(yyout, "RESTA "); }
"*"                               { fprintf(yyout, "MULT "); }
"/"                               { fprintf(yyout, "DIV "); }
"%"                               { fprintf(yyout, "MOD "); }

[ \t\n]+                          { fprintf(yyout, "%s", yytext); }
.                                 { fprintf(yyout, "%s", yytext); }
%%

int main(void) {
    yyin  = fopen("programa.txt", "r");
    yyout = fopen("out.txt", "w");

    if (!yyin)  { perror("No se pudo abrir programa.txt"); return 1; }
    if (!yyout) { perror("No se pudo abrir out.txt");      return 1; }

    yylex();

    fclose(yyin);
    fclose(yyout);
    return 0;
}
