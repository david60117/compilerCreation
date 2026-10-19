%{
#include "parser.tab.h"
int linea = 1;
#define YY_USER_ACTION yylloc.first_line = yylloc.last_line = linea;
%}
%option noyywrap

%%
ENTERO                            { return TIPO_ENT; }
FLOTANTE                          { return TIPO_FLOT; }
CADENA                            { return TIPO_STRING; }
CARACTER                          { return TIPO_CARACTER; }
LOGICO                            { return TIPO_LOGICO; }
MIENTRAS                          { return WHILE; }
PARA                              { return FOR; }
ESCRIBIR                          { return PRINT; }

SI                                { return SI; }
SINO                              { return SINO; }

VERDADERO                         { return VERDADERO; }
FALSO                             { return FALSO; }

["][^"\n]*["]                     { return CADENA; }
[0-9]+([.][0-9]+)?                { return NUMERO; }
[a-zA-Z_][a-zA-Z0-9_]*            { return VARIABLE; }

"=="                              { return IGUAL; }
"!="                              { return DIFERENTE; }
"<="                              { return MENOR_IGUAL; }
">="                              { return MAYOR_IGUAL; }
"<"                               { return MENOR; }
">"                               { return MAYOR; }

"&&"                              { return AND; }
"||"                              { return OR; }
"!"                               { return NOT; }

"="                               { return ASIGNACION; }

"+"                               { return SUMA; }
"-"                               { return RESTA; }
"*"                               { return MULT; }
"/"                               { return DIV; }
"%"                               { return MOD; }

\n                                { linea++; return NL; }
[ \t\r]+                          { }
.                                 { return yytext[0]; }
<<EOF>>                           { static int fin = 0; if (!fin) { fin = 1; return NL; } return 0; }
%%
