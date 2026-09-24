Estructura del proyecto


C:.
│   agente.py
│   main.py
│   README.txt
│   
├───Agente_Cazador
│       agente.py
│       memoria.py
│       sentidos.py
│       
├───Algoritmos
│       a_Estrella.py
│       huida.py
│       persecucion.py
│       
├───Interfaz
│   │   interfaz.py
│   │   
│   └───__pycache__
│           interfaz.cpython-313.pyc
│           
├───Mundo
│   │   mundo.py
│   │   
│   └───__pycache__
│           mundo.cpython-313.pyc
│           
└───Recursos
    │   arbol.py
    │   arena.py
    │   bayas.py
    │   campamento.py
    │   cazador.py
    │   puma.py
    │   raton.py
    │   
    └───__pycache__
            arbol.cpython-313.pyc
            arena.cpython-313.pyc
            bayas.cpython-313.pyc
            campamento.cpython-313.pyc
            cazador.cpython-313.pyc


Estructura del proyecto

El proyecto está organizado en diferentes carpetas para separar las funciones principales 
del agente inteligente y facilitar su desarrollo y mantenimiento.

-main.py: Es el archivo principal que inicia la ejecución del programa y pone en funcionamiento la interfaz.
-agente.py: Archivo ubicado en la raíz del proyecto. Se utiliza como base para saber como separar el proyecto.-agente general-
-README.txt: Contiene la información y documentación básica del proyecto.

`Agente_Cazador/`

Contiene los componentes que forman el agente cazador y permiten que pueda percibir, recordar información y tomar decisiones.

-`agente.py`**: Contiene la lógica principal del agente cazador y sus decisiones.
-`memoria.py`**: Se encarga de almacenar la información que el agente obtiene durante la exploración del mundo.
-`sentidos.py`**: Maneja las percepciones que recibe el agente sobre su entorno (vista, oído, tacto, gusto y olfato).

`Algoritmos/`

Contiene los algoritmos utilizados para controlar diferentes comportamientos y formas de desplazamiento del agente.

-`a_Estrella.py`: Contiene el algoritmo A* para encontrar rutas dentro del tablero.
-`huida.py`: Contiene la lógica relacionada con el comportamiento de huida.
-`persecucion.py`: Contiene la lógica relacionada con la persecución de otros elementos del mundo.

`Interfaz/`
Contiene los elementos encargados de mostrar visualmente el mundo y la información del agente.

-`interfaz.py`: Crea la ventana del programa, dibuja el tablero, muestra información como energía, vidas y estado,
 y utiliza los recursos gráficos para representar el mundo.

`Mundo/`
Contiene la lógica que representa el entorno donde se desarrolla la simulación.

-`mundo.py`: Genera el tablero, administra las posiciones de los elementos, define los tipos de terreno, 
comprueba colisiones y proporciona las percepciones de las celdas cercanas.

`Recursos/`
Contiene las clases encargadas de dibujar los diferentes elementos que aparecen dentro del mundo.

-`arbol.py`: Dibuja los árboles.
-`arena.py`: Dibuja la arena movediza.
-`bayas.py`: Dibuja las bayas buenas y malas.
-`campamento.py`: Dibuja el campamento.
-`cazador.py`: Dibuja al cazador.
-`puma.py`: Dibuja al puma.
-`raton.py`: Dibuja al ratón.

Sentidos del agente

El agente cazador percibe el mundo con cinco sentidos. Todos están en `Agente_Cazador/sentidos.py`
y se muestran en el panel superior de la interfaz.

-Vista: Ve hasta 2 casillas de distancia. Los árboles tapan la vista: si hay un árbol entre el cazador
 y una casilla, no la puede ver (en diagonal solo se tapa si los dos lados son árboles).
 Además de buscar al puma, se fija en el terreno que tiene enfrente y guarda en memoria dónde hay
 arena movediza y bayas. De las bayas solo ve el color (moradas o rojas): no sabe si son buenas
 o malas hasta que las prueba.
-Oído: Escucha al puma hasta 3 casillas, aunque haya árboles en medio (el sonido sí pasa entre ellos).
 Solo se usa cuando no lo puede ver. Da la dirección del sonido en 8 direcciones
 (NORTE, SUR, ESTE, OESTE, NORESTE, NOROESTE, SURESTE, SUROESTE) y su intensidad:
 "fuerte" si está a menos de 3 casillas y "débil" si está a 3.
-Olfato: Tiene dos usos.
 1. Puma: lo huele a 4 o 5 casillas. A 4 casillas es "Olor fuerte" y a 5 es "Olor débil".
    No da la posición exacta, solo hacia qué casilla vecina el olor es más fuerte, y el agente sigue ese rastro.
    Si los árboles bloquean el rastro, el agente sigue explorando.
 2. Bayas: huele las bayas a 3 casillas o menos, pero solo sigue el olor de un color que ya aprendió
    que es bueno. Lo usa cuando tiene poca energía.
-Tacto: Siente el terreno donde está parado ("Suelo firme" o "Arena movediza") y también la arena
 de las casillas vecinas (norte, sur, este y oeste) antes de pisarla. La arena que siente se guarda en memoria.
-Gusto: Prueba las bayas que encuentra: "Bayas dulces" (+20 de energía) o "Bayas amargas" (-10 de energía).
 Es el sentido con el que el agente aprende: al probar una baya, recuerda si ese color es bueno o malo
 (ver "Aprendizaje de las bayas"). Cuando se come una baya, la olvida de la memoria.

Aprendizaje de las bayas

Al inicio el agente no sabe qué bayas son buenas y cuáles son malas. Aprende de su experiencia:
1. Con la vista solo distingue el color: moradas o rojas.
2. Cuando pisa una baya, se la come y el gusto le dice si es dulce (+20) o amarga (-10).
3. Guarda en memoria ese color como "buena" o "mala" y en el estado aparece, por ejemplo,
   "¡Aprendió: bayas rojas son malas! (-10)".
4. Desde ese momento aplica lo aprendido a todas las bayas de ese color:
   evita las de color malo y, con poca energía, busca las de color bueno.

Por eso siempre tiene que comer al menos una baya mala para aprender a evitarlas.
En el mundo actual las moradas son buenas y las rojas son malas.

Memoria del terreno (`Agente_Cazador/memoria.py`)

Además de las celdas revisadas y la última posición del puma, la memoria guarda:
-Bayas que ha visto y de qué color son.
-Lo que ha aprendido de cada color de baya: "buena", "mala" o todavía sin probar.
-Arena movediza que ha visto o sentido.

Con esta memoria el agente:
-Evita pisar las bayas de un color que ya aprendió que es malo. El A* (`Algoritmos/a_Estrella.py`) les pone un costo alto
 para rodearlas si hay otro camino.
-No elige esas bayas como destino al explorar.
-Cuando tiene poca energía, va por una baya de color bueno que recuerda si está más cerca que el campamento.

Prioridad de decisiones del agente:
1. Si tiene poca energía (menos de 30):
   a. Si recuerda una baya de color bueno más cerca que el campamento, va por ella.
   b. Si no, pero huele bayas de color bueno y el campamento está lejos, sigue ese olor.
   c. Si no, regresa al campamento.
2. Si ve al puma, lo persigue.
3. Si lo escucha, va hacia la dirección del sonido.
4. Si lo huele, sigue el rastro del olor.
5. Si recuerda dónde lo vio, va a investigar esa posición.
6. Si no percibe nada, explora zonas que todavía no ha revisado.

Después de moverse una casilla, el agente vuelve a usar la vista, el oído y el olfato desde su nueva
posición. Así todo lo que muestra el panel (vista, oído, olfato, tacto y gusto) corresponde a la casilla
donde está parado en ese momento.

Panel de la interfaz

-Fila 1: Energía y estado del agente.
-Fila 2: Vista, Oído (dirección e intensidad) y Memoria (celdas revisadas).
-Fila 3: Tacto, Gusto y Olfato (puma o bayas de color bueno).
-Fila 4: Controles, Arena cerca (N, S, E, O) y lo que ha aprendido de las bayas
 ("Moradas: buena  Rojas: mala"; "?" si todavía no las prueba).

Las carpetas `__pycache__` contienen archivos temporales generados automáticamente por Python al ejecutar el programa. 
Estos archivos no forman parte de la lógica principal del proyecto.
