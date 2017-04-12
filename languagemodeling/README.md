TRABAJO PRÁCTICO 1: MODELADO DE LENGUAJE
========================================

Ejercicio 1
-----------

>  El corpus elegido consta de 10 novelas, 1 memoria y 4 cuentos de Gabriel
>García Márquez. El corpus de texto tiene un tamaño de 5,5MB de tamaño.

### Tokenización y segmentado de oraciones
>  Se utiliza un "corpus reader" de NLTK, precisamente "PlaintextCorpusReader".
>Además, se usa el tokenizador "RegexpTokenizer", también de NLTK, con un
>patrón que detecta abreviaciones (e.g. U.S.A), palabras (que también pueden
>contener un guión medio), valores de dinero o porcentajes (e.g. $12.50, 76%),
>los puntos suspensivos, y diferentes símbolos (e.g. "[", "]", "?", ";", etc).
>Se agregaron ciertas expresiones específicas como "Inc.", "Sr." o "Sra." para
>comprobar la correcta tokenización de ejemplos de corpus particulares, aunque >específicamente con el corpus elegido, no es necesario, ya que estas
>expresiones no aparecen (de todos modos, se lo deja en el patrón).
