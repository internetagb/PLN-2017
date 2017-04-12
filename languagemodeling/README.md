TRABAJO PRÁCTICO 1: MODELADO DE LENGUAJE
========================================

Ejercicio 1
-----------

>El corpus elegido consta de 10 novelas, 1 memoria y 4 cuentos de Gabriel
>García Márquez. El corpus de texto tiene un tamaño de 5,5MB de tamaño.
>Todo los textos están en su idioma original (español).

### Tokenización y segmentado de oraciones
>  Se utiliza un "corpus reader" de NLTK, precisamente *PlaintextCorpusReader*.
>Además, se usa el tokenizador *RegexpTokenizer*, también de NLTK, con un
>patrón que detecta abreviaciones (e.g. U.S.A), palabras (que también pueden
>contener un guión medio), valores de dinero o porcentajes (e.g. $12.50, 76%),
>los puntos suspensivos, y diferentes símbolos (e.g. "[", "]", "?", ";", etc).
>Se agregaron ciertas expresiones específicas como "Inc.", "Sr." o "Sra." para
>comprobar la correcta tokenización de ejemplos de corpus particulares, aunque
>específicamente con el corpus elegido, no es necesario, ya que estas
>expresiones no aparecen (de todos modos, se lo deja en el patrón).


Ejercicio 2
-----------

>El analisis, se hace trabajando con la *supocición de Markov*,
>para calcular las probabilidades necesarias, utilizando el modelo de n-gramas.

>Para implementarlo, se hace una clase "NGram", utilizando marcadores de
>comienzo y final de oración (<s> y </s> respectivamente).

### Idea general de la clase NGram
>Describiremos brevemente lo que se hizo para que NGram cumpla su objetivo.

#### Inicialización
>Se necesita saber con que orden de modelo de n-gramas se va a
>trabajar, es decir, el valor de 'n', y conocer las oraciones que se van a
>analizar.
>Lo que hace es contar la cantidad de veces que ocurre cada n-grama y
>(n-1)-grama correspondientes a las oraciones ingresadas, para posibilitar el
>calculo de probabilidades.

#### Conteos de ocurrencias y probabilidades
>Conociendo la cantidad de veces que ocurren los n-gramas y (n-1)-gramas
>(hecho en "Inicialización"), es posible calcular la probabilidad de
>ocurrencia de una palabra, dado que ocurrieron ciertas (n-1) palabras
>anteriores (Recordad que usamos *"Markov Assumption"*).
>Esto nos sirve para saber que probabilidad tiene una oración completa de
>ocurrir, multiplicando solo las probabilidades de ocurrencia de los n-gramas
>correspondientes.
>Estas probabilidades, suelen llegar a valores muy pequeños, pudiendo ocasionar
>*"underflow"*. Para evitar eso se realiza el calculo de *"log-probability"*,
>aprovechando también el hecho de que sumar es mas rápido que multiplicar.



>Todo esto, nos deja las herramientas necesarias para poder generar oraciones
>de lenguaje natural y además, poder evaluar modelos entrenados.












