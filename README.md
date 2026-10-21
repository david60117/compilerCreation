## Instalaciones necesarias (solo Linux Ubuntu)

- flex
- bison
- graphviz

```bash
sudo apt update
sudo apt install flex
sudo apt install bison
sudo apt install graphviz
```

## Instalaciones adicionales

```bash
sudo apt install build-essential
sudo apt install nano
```

- `build-essential` incluye `gcc` y las librerías de C necesarias para compilar.
- `nano` es un editor de texto en terminal para modificar los archivos.

## Pasos

1. Creación del archivo `lexer.l` (analizador léxico).
2. Creación del archivo `parser.y` (analizador sintáctico).
3. Creación de los archivos `ast.c` y `ast.h` (construcción del árbol de sintaxis abstracta).

## Cómo ejecutar mediante terminal

1. Generar el analizador léxico (crea `lex.yy.c`):
```bash
   flex lexer.l
```
2. Generar el analizador sintáctico (crea `parser.tab.c` y `parser.tab.h`):
```bash
   bison -d parser.y
```
3. Compilar todo en el ejecutable `programa`:
```bash
   gcc lex.yy.c parser.tab.c ast.c -o programa
```
4. Ejecutar `programa` leyendo de `programa.txt`. `tee` muestra la salida en pantalla y además la guarda en `out.txt`:
```bash
   ./programa < programa.txt | tee out.txt
```
5. Convertir `ast.dot` en la imagen `ast.png` con Graphviz. `-Tpng` indica el formato de salida y `-o` el nombre del archivo:
```bash
   dot -Tpng ast.dot -o ast.png
```

## Ejecución en Windows

Los comandos de instalación anteriores son solo para Linux Ubuntu. En Windows, con flex, bison, gcc y graphviz instalados, los comandos de ejecución son los mismos usando una terminal tipo bash (Git Bash o MSYS2). Solo cambia el nombre del ejecutable:

```bash
flex lexer.l
bison -d parser.y
gcc lex.yy.c parser.tab.c ast.c -o programa.exe
./programa.exe < programa.txt | tee out.txt
dot -Tpng ast.dot -o ast.png
```
