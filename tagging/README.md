TRABAJO PRÁCTICO 2: ETIQUETADO DE SECUENCIAS
============================================

Ejercicio 1: Corpus AnCora: Estadísticas de etiquetas POS
---------------------------------------------------------

>Se hace un análisis estadístico de etiquetas del Corpus AnCora.
>Los resultados de este análisis se mostrarán a continuación.

### Estadísticas básicas
>Cantidad de oraciones: **17378**  
>Cantidad de ocurrencias de palabras: **517194**  
>Cantidad de tipos de palabras: **46501**  
>Cantidad de etiquetas: **85**  


### Etiquetas mas frecuentes

| Tag | Frecuencia | Porcentaje | 5 palabras mas frecuentes |
| :---: | :---: | :---: | :---: |
| sp000   |    79884     |  15.446 %  | de, en, a, del, con                    |
|nc0s000  |    63452     |  12.269 %  | presidente, equipo, partido, país, año |
| da0000  |    54549     |  10.547 %  | la, el, los, las, El                   |
| aq0000  |    33906     |  6.556 %   | pasado, gran, mayor, nuevo, próximo    |
|   fc    |    30147     |  5.829 %   | ,                                      |
|np00000  |    29111     |  5.629 %   | Gobierno, España, PP, Barcelona, Madrid|
|nc0p000  |    27736     |  5.363 %   | años, millones, personas, países, días |
|   fp    |    17512     |  3.386 %   | .                                      |
|   rg    |    15336     |  2.965 %   | más, hoy, también, ayer, ya            |
|   cc    |    15023     |  2.905 %   | y, pero, o, Pero, e                    |

#### Descripción de etiquetas
> **sp000:** preposición (tag único, es decir no hay otro tipo de preposiciones).  
> **nc0s000:** sustantivo común singular.  
> **da0000:** artículo definido.  
> **aq0000:** adjetivo descriptivo.  
> **fc:** coma ("**,**").  
> **np00000:** sustantivo propio.  
> **nc0p000:** sustantivo común plural.  
> **fp:** punto ("**.**").  
> **rg:** adverbio general  
> **cc:** conjuncion coordinada.  


### Niveles de ambigüedad


| Nivel de ambigüedad |  Cantidad  | Porcentaje |  5 palabras mas frecuentes|
| :---: | :---: | :---: | :---: |
|         1           |   43972    |  94.561 %  | , , con, por, su, El |
|         2           |    2318    |  4.985 %   | el,en, y, ", los |
|         3           |    180     |  0.387 %   | de, la, ., un, no |
|         4           |     23     |  0.049 %   | que, a, dos, este, fue |
|         5           |     5      |  0.011 %   | mismo, cinco, medio, ocho, vista|
|         6           |     3      |  0.006 %   | una, como, uno |
|         7           |     0      |   0.0 %    | |
|         8           |     0      |   0.0 %    | |
|         9           |     0      |   0.0 %    | |


Ejercicio 2: Baseline Tagger
----------------------------

>El objetivo es etiquetar las palabras de alguna manera, es decir, hacer un
>etiquetador.
>Lo que se hace, en la etapa de entrenamiento, es ver cual es el *tag* mas
>frecuente con el que se etiqueta a cada palabra.
>Ese, es el *tag* con el que se etiquetará a la palabra correspondiente.
>A estos *tags*, desde el punto de vista de implementación, los obtenemos
>contando, para las etiquetas de cada palabra, cuantas veces ocurre cada una,
>y seleccionamos la de mayor número de ocurrencias.
>Finalmente, a esta información la guardamos en un diccionario, donde las
>claves corresponden a las palabras, y los valores, al *tag* mas frecuente
>con el que se etiqueta a esa palabra.
>Al momento de etiquetar, busco en este diccionario, el valor de esa
>palabra, y si me encuentro con una palabra que no esta en el diccionario,
>es decir, una palabra no vista durante el entrenamiento (*unknown*),
>la etiquetamos con un *tag* determinado, específicamente, *nc0s000*.

Ejercicio 3: Entrenamiento y Evaluación de Taggers
--------------------------------------------------

>Usando el etiquetador *Baseline*, puede haber errores al momento de etiquetar
>palabras.
>Vamos a analizar el porcetaje de etiquetado correcto sobre el total de
>palabras y también sobre las palabras conocidas y desconocidas.
>También se calculará una *matriz de confusión*, para mostrar en que porcentaje
>una palabra con etiqueta *x* se etiquetó incorrectamente con etiqueta *y*.

### Resultados obtenidos

>Precisión general: 87.59%  
>Precisión para palabras desconocidas: 18.01%  
>Precisión: 95.27%

#### Matriz de confusión

|  | sp000 | nc0s000 | da0000 | aq0000 | fc | nc0p000 | rg | np00000 | fp | cc |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **sp000** | 14.284 | 0.047 | 0.0 | 0.0 | 0.0 | 0.0 | 0.005 | 0.0 | 0.0 | 0.0 |
| **nc0s000** | 0.002 | 12.241 | 0.0 | 0.234 | 0.0 | 0.001 | 0.025 | 0.001 | 0.0 | 0.001 |
| **da0000** | 0.0 | 0.151 | 9.543 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **aq0000** | 0.005 | 2.061 | 0.0 | 4.839 | 0.0 | 0.135 | 0.003 | 0.0 | 0.0 | 0.0 |
| **fc** | 0.0 | 0.0 | 0.0 | 0.0 | 5.85 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| **nc0p000** | 0.0 | 1.237 | 0.0 | 0.182 | 0.0 | 4.102 | 0.0 | 0.0 | 0.0 | 0.0 |
| **rg** | 0.018 | 0.314 | 0.0 | 0.044 | 0.0 | 0.0 | 3.269 | 0.0 | 0.0 | 0.022 |
| **np00000** | 0.003 | 2.039 | 0.0 | 0.001 | 0.0 | 0.003 | 0.0 | 1.523 | 0.0 | 0.001 |
| **fp** | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 3.55 | 0.0 |
| **cc** | 0.001 | 0.014 | 0.0 | 0.0 | 0.0 | 0.0 | 0.049 | 0.001 | 0.0 | 3.341 |

Ejercicio 4: Hidden Markov Models y Algoritmo de Viterbi
--------------------------------------------------------

### Hidden Markov Models (HMM)

>Se quiere calcular la probabilidad conjunta de una oración y una secuencia
>de *tags*, es decir la probabilidad de que una oración sea etiquetada con esa
>secuencia.
>Para esto, utilizamos la supocición de Markov, para calcular la probabilidad
>de que ocurra un *tag*, dado que ocurrieron ciertos *tags* previos, y además,
>la probabilidad de que ocurra la palabra dado el *tag* (para cada par de
>etiqueta y palabra).
>Desde el punto de vista implementación, esto se calcula en la clase HMM,
>ingresandole los valores de tamaño de n-grama, tags, probabilidades de
>transición y probabilidades de palabras dado un cierto tag.

### Algoritmo de Viterbi

>Este algoritmo busca encontrar cual es el etiquetado más probable de una
>oración sin tener que revisar todas las combinaciones posibles que hay entre
>los *tags*.
>Para esto, se va calculando cual es la probabilidad de tags mas alta hasta el
>momento, y ahí, se analiza cual es el siguiente *tag* que da la probabilidad
>más alta.
>Cuando se llega al final de la oración, elegimos los n-1 *tags* que tienen más
>probabilidad de etiquetar el final de la oración (trabajando con n-gramas).

>Al momento de implementar, la información de la probabilidad más alta hasta el
>momento se guarda en un diccionario de diccionarios, con el nombre de la letra
>griega *pi*.
>Las *keys* de este diccionario *pi*, corresponden a la posición de la oración
>cuya probabilidad y etiquetado hasta ese momento, se ve en sus *values*.
>Con estos datos, queremos ver cual es el *tag* que hace que la probabilidad
>hasta el momento junto con la de agregar este *tag* sea la más alta.
>Para esto debemos calcular las probabilidades con cada una de las etiquetas
>posibles, y elegir la probabilidad mayor (junto con la etiqueta que hizo que
>esta probabilidad sea la mayor).
>De esta forma se van eligiendo los *tags* más probables hasta llegar al final
>de la oración, en donde se eligen los *tags* para el final de oración, que se
>obtienen de la misma manera que antes.


Ejercicio 5: HMM POS Tagger
---------------------------

>Implementamos la clase MLHMM, en donde los parámetros se estiman usando
>Maximun Likelihood. Además tenemos la opción de usar *addone smoothing*.

>Entrenamos el modelo y lo evaluamos para uni-gramas, bi-gramas, tri-gramas y
>cuatri-gramas.
>Los resultados se muestran a continuación.

| n | Precisión Total | Precisión de palabras conocidas | Precisión de palabras desconocidas | Tiempo de evaluación |
| :---: | :---: | :---: | :---: | :---: |
| 1 | 85.84% | 95.28% | 0.45% | 0 min 15.5 seg |
| 2 | 91.34% | 97.63% | 34.33% | 0 min 30.7 seg |
| 3 | 91.86% | 97.65% | 39.49% | 2 min 49.6 seg |
| 4 | 91.61% | 97.31%% | 40.01% | 21 min 54.4 seg |


Ejercicio 6: Features para Etiquetado de Secuencias
---------------------------------------------------

>Implementamos diferentes *features*, que dada una *history*, analizamos:
>- La palabra actual está en minúsculas.
>- La palabra actual empieza en mayúscula.
>- La palabra actual está en mayúsculas.
>- La palabra actual es un número.

>También definimos *features* con parámetros:
>- La tupla de los últimos **n** *tags*.
>- Aplicar un *feature* **f** a la palabra anterior a la actual.

>Recordamos que la *history* contiene la oración completa y los *tags* previos,
>por eso podemos definir estas *features*.


Ejercicio 7: Maximum Entropy Markov Models
------------------------------------------

