/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif
/* "%code requires" blocks.  */
#line 1 "parser.y"

#include "ast.h"

#line 53 "parser.tab.h"

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    TIPO_ENT = 258,                /* TIPO_ENT  */
    TIPO_FLOT = 259,               /* TIPO_FLOT  */
    TIPO_STRING = 260,             /* TIPO_STRING  */
    TIPO_CARACTER = 261,           /* TIPO_CARACTER  */
    TIPO_LOGICO = 262,             /* TIPO_LOGICO  */
    WHILE = 263,                   /* WHILE  */
    FOR = 264,                     /* FOR  */
    PRINT = 265,                   /* PRINT  */
    SI = 266,                      /* SI  */
    SINO = 267,                    /* SINO  */
    VERDADERO = 268,               /* VERDADERO  */
    FALSO = 269,                   /* FALSO  */
    CADENA = 270,                  /* CADENA  */
    NUMERO = 271,                  /* NUMERO  */
    VARIABLE = 272,                /* VARIABLE  */
    ASIGNACION = 273,              /* ASIGNACION  */
    NL = 274,                      /* NL  */
    OR = 275,                      /* OR  */
    AND = 276,                     /* AND  */
    IGUAL = 277,                   /* IGUAL  */
    DIFERENTE = 278,               /* DIFERENTE  */
    MENOR = 279,                   /* MENOR  */
    MAYOR = 280,                   /* MAYOR  */
    MENOR_IGUAL = 281,             /* MENOR_IGUAL  */
    MAYOR_IGUAL = 282,             /* MAYOR_IGUAL  */
    SUMA = 283,                    /* SUMA  */
    RESTA = 284,                   /* RESTA  */
    MULT = 285,                    /* MULT  */
    DIV = 286,                     /* DIV  */
    MOD = 287,                     /* MOD  */
    NOT = 288                      /* NOT  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 17 "parser.y"
 char *str; Nodo *nodo; 

#line 106 "parser.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif


extern YYSTYPE yylval;
extern YYLTYPE yylloc;

int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
