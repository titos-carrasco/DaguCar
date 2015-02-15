#DaguCar/iRacer

Código para controlar el auto DaguCar/iRacer (bluetooth)

Mayor información puede ser encontrada en
[sparkfun](https://www.sparkfun.com/products/11162). En particular existe
un problema con la bateria que deja de cargar después de cierto tiempo.
Para solucionarlo, aplicar directamente 5V a los pines de la bateria
(ver conectores + y - en la placa al costado del botón de encendido)

El directorio Doc/ contiene un archivo PDF con los comandos que controlan
al auto

El directorio Python/ contiene el código en Python

El directorio Cpp/ contiene el código en C++

El directorio Java/ contiene el código en Java

***
###Historia
* Jan 15, 2015: Agrega código Java y realiza correcciones menores en código
Python. El código Java es trabajado en Geany (ver Java.geany en el directorio)
* Nov 13, 2014: Todos los textos a español, corrige código ante errores de
apertura serial. Se cambia el widget GtkSwitch por un toggle button ante
errores de procesamiento en evento Activate
* May 1, 2014: Se mueve el código al directorio Python/ y se inicia
la versión C++
* Abr 13, 2014: agrega documentación en línea y reescribe código
* Abr 7, 2014: Cambios cosméticos
* Mar 30, 2014: Agrega interface en Glade para testear el código
* Mar 8, 2014: Commit inicial. Se mueve el código desde GoogleCode a GitHub
