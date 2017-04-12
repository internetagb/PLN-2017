TRABAJO PRÁCTICO 1: MODELADO DE LENGUAJE
========================================

Ejercicio 1
-----------

>El corpus elegido consta de 10 novelas, 1 memoria y 4 cuentos de Gabriel
>García Márquez. El corpus de texto tiene un tamaño de 5,5MB de tamaño.
>Todo los textos están en su idioma original (español).

### Tokenización y segmentado de oraciones
>Se utiliza un "corpus reader" de NLTK, precisamente *PlaintextCorpusReader*.
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
>calculo de probabilidades. Estas "cantidades" se guardan en un "diccionario".

#### Conteos de ocurrencias y probabilidades
>Conociendo la cantidad de veces que ocurren los n-gramas y (n-1)-gramas
>(hecho en "Inicialización"), es posible calcular la probabilidad de
>ocurrencia de una palabra, dado que ocurrieron ciertas (n-1) palabras
>anteriores (Recordar que usamos *"Markov Assumption"*).
>En definitiva, lo que se hace ver (del diccionario) la cantidad de veces que
>"ocurre un n-grama" y se lo divide por la cantidad de veces que
>"ocurre el (n-1)-grama" correspondiente.
>Esto nos sirve para saber que probabilidad tiene una oración completa de
>ocurrir, multiplicando solo las probabilidades de ocurrencia de los n-gramas
>necesarios, que participan en la oración.
>Estas probabilidades, suelen llegar a valores muy pequeños, pudiendo ocasionar
>*"underflow"*. Para evitar eso se realiza el calculo de *"log-probability"*,
>aprovechando también el hecho de que sumar es mas rápido que multiplicar.
>Se calcula sumando los logaritmos (base 2) de las probabilidades calculadas
>anteriormente.


Ejercicio 3
-----------

>Todo lo anterior, nos dejó las herramientas necesarias para poder generar
>oraciones de lenguaje natural.
>Lo que haremos es describir como se generan, esas oraciones y además mostrar
>algunos ejemplos de lo generado.

### Entrenamiento previo
>Para poder generar oraciones, es necesario tener algunas referencias a la
>hora de "crear". Esto se consigue con el *"entrenamiento"*, que es posible
>gracias a las herramientas que provee NGram.
>El "entrenamiento" en sí, es hacer todo el trabajo que se describió en
>*Ejercicio 2*, para que (mediante las probabilidades), pueda ir eligiendo las
>palabras para generar la oración.
>Esto se hace justamente en  el script *train.py*, y con el script
>*generate.py* se carga el modelo de n-gramas, y se genera oraciones con él.

### Generación de oraciones
>Se implementa la clase *NGramGenerator*, cuyo trabajo es ir eligiendo palabras
>para luego unirlas y formar una oración.
>Primero que nada debemos conocer esas "probabilidades" necesarias para tomar
>la decisión de que palabras elegir.
>Utilizamos la estructura de diccionarios para tener estos datos almacenados.
>Lo que se guarda es, las probabilidades de qué palabra puede seguir luego de
>ciertas palabras anteriores (esto se hace en la inicialización de la clase).
>Para cumplir con estas probabilidades al momento de elegir palabras, se usa
>el *Método de la transformación inversa*.
>A medida que voy eligiendo palabras, las voy agregando a la oración (que
>se tiene en ese instante) hasta que aparezca un final de oración, detectado
>con el delimitador '</s>'.


### Ejemplos de oraciones generadas

##### Unigramas

>Todos o las . el en cuando casa actividad y cubiertos como . de El que

>precisó los prosiguió de la dormitorio del encima pero . planchados dijo
>mecerse mano tu como como tuviera de vaca acostó sirvienta encargarán en . una

>le la escuchan cama


#### Bigramas

>No hay sino que me había albergue de siempre la situación .

>Por la escasez que era un chorro del día y los ojos desolados , semejantes
>engaños , Miranda , se mantenía por casualidad con veinte años , vigilaba la
>péndola de sal en seguida el nuestro entierro , porque las artesas del sol ,
>donde estaba , padre Ángel , tenía el eco con lápiz en ella mantuvo alerta y
>mordisqueando el dueño y se acostó en los fondos de que tuvo consuelo para
>ver que las gallinas se había que el olor .

>Sentí una de Ayapel , era de la reunión del buque .


#### Trigramas

>Sin embargo , se sentaron a la pelota en el bochorno de mayo comulgó
>torturado por el encierro terminara con las primeras sombras tratando de
>mantener vivos los ojos atigrados por las fogatas .

>Elaboré un intrincado frangollo de verdades contradictorias que parecían ,
>sino con todos los días .

>Era el más difícil de este mundo dos hombres fumando sentados en círculo bajo
>el mohoso palio de lonas amarillas .


#### Cuatrigramas

> Se rompió los puños contra los muros de argamasa de El Niño de Oro , una
>tienda de cam-paña que le habían puesto un pasquín verídico contra su hija
>soltera .


>Nos pareció un golpe de suerte inconcebible , porque en casos como ése me
>dieron una canonjía en las oficinas del buque era tan seductor que no tuve
>corazón para venderlos .

>El único vínculo que le quedó de aquel descalabro a Florentino Ariza en su
>primer viaje a Europa .




> A medida que aumenta el tamaño de los n-gramas, las oraciones generadas,
>cobran mas sentido, desde el caso de unigramas, que simplemente es un sorteo
>aleatorio de palabras, hasta los cuatrigramas, que ya generan oraciones con
>mucho más sentido.
> Si el n es muy grande, las oraciónes tendrán mucho sentido (a no ser que las
>del corpus original no lo tengan), ya que serán prácticamente las oraciones
>tal cual aparecen en el corpus.



























