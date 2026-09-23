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
-`sentidos.py`**: Maneja las percepciones que recibe el agente sobre su entorno.

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

Las carpetas `__pycache__` contienen archivos temporales generados automáticamente por Python al ejecutar el programa. 
Estos archivos no forman parte de la lógica principal del proyecto.
