Estructura del proyecto


C:.
│   agente.py
│   main.py
│   README.txt
│   .gitignore
│
├───Agente_Cazador
│       agente.py
│       memoria.py
│       sentidos.py
│
├───Agente_Jaguar
│       agente.py
│
├───Algoritmos
│       a_Estrella.py
│       huida.py
│       persecucion.py
│
├───Fisica
│       cinematica.py
│
├───Interfaz
│       interfaz.py
│
├───Mundo
│       mundo.py
│
└───Recursos
    │   arbol.py
    │   arena.py
    │   bayas.py
    │   campamento.py
    │   cazador.py
    │   jaguar.py
    │   raton.py
    │
    └───images
            (sprites .png)

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

-`a_Estrella.py`: Contiene el algoritmo A* para encontrar rutas dentro del tablero. Usa costos por suelo
 y una lista de nodos cerrados para no expandir dos veces el mismo nodo.
-`huida.py`: Comportamiento de escape. El jaguar elige la casilla vecina que más lo aleja del cazador,
 prefiriendo casillas con varias salidas (para no quedar acorralado) y evitando la arena.
-`persecucion.py`: Comportamiento de persecución. Calcula un punto de intercepción: en lugar de ir
 a donde está el jaguar, el cazador apunta a donde va a estar, según la dirección en que se mueve.

`Agente_Jaguar/`

-`agente.py`: El jaguar también es un agente. Detecta al cazador a 4 casillas (lo huele y lo oye, los árboles
 no lo tapan). Si lo detecta, huye usando `huida.py`. Si no, descansa o merodea al azar (evitando la arena
 y el campamento). Si ninguna casilla lo aleja, queda "Acorralado".

`Fisica/`

-`cinematica.py`: Masa y física cinemática del cazador y del jaguar (ver "Masa y física cinemática").

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
-`bayas.py`: Dibuja las bayas buenas (rojas) y malas (azules).
-`campamento.py`: Dibuja el campamento.
-`cazador.py`: Dibuja al cazador. El sprite cambia según la dirección en la que se mueve.
-`jaguar.py`: Dibuja al jaguar (sprite de jaguar). El sprite cambia según la dirección en la que se mueve.
-`raton.py`: Dibuja al ratón.
-`images/`: Sprites (imágenes .png) que usan las clases anteriores: árbol, arena movediza,
 bayas buenas y malas, campamento, ratón, y el cazador y el jaguar en 4 direcciones
 (arriba, abajo, izquierda y derecha).

Sentidos del agente

El agente cazador percibe el mundo con cinco sentidos. Todos están en `Agente_Cazador/sentidos.py`
y se muestran en el panel superior de la interfaz.

Alcance de cada sentido (se cambia en el __init__ de `sentidos.py`):
-Vista: 4 casillas (`rango_vista`).
-Oído: 2 casillas (`rango_oido`).
-Olfato: 1 casilla (`rango_olfato`), para el jaguar y para las bayas.

Cada sentido detecta al jaguar por su cuenta, dentro de su propio alcance. Por eso pueden detectarlo
varios sentidos al mismo tiempo (por ejemplo, a 1 casilla lo ve, lo oye y lo huele). Para decidir,
el agente usa primero la vista, después el oído y al final el olfato.

-Vista: Ve hasta 4 casillas de distancia. Los árboles tapan la vista: si hay un árbol entre el cazador
 y una casilla, no la puede ver (en diagonal solo se tapa si los dos lados son árboles).
 Además de buscar al jaguar, se fija en el terreno que tiene enfrente y guarda en memoria dónde hay
 arena movediza y bayas. De las bayas solo ve el color (rojas o azules): no sabe si son buenas
 o malas hasta que las prueba.
-Oído: Escucha al jaguar hasta 2 casillas, aunque haya árboles en medio (el sonido sí pasa entre ellos).
 Es útil cuando un árbol le tapa la vista. Da la dirección del sonido en 8 direcciones
 (NORTE, SUR, ESTE, OESTE, NORESTE, NOROESTE, SURESTE, SUROESTE) y su intensidad:
 "fuerte" a 1 casilla y "débil" a 2.
-Olfato: Tiene dos usos.
 1. Jaguar: lo huele a 1 casilla ("Olor fuerte"). El olor pasa entre los árboles.
    No da la posición exacta, solo hacia qué casilla vecina el olor es más fuerte, y el agente sigue ese rastro.
    Si los árboles bloquean el rastro, el agente sigue explorando.
 2. Bayas: huele las bayas a 1 casilla, pero solo sigue el olor de un color que ya aprendió
    que es bueno. Lo usa cuando tiene poca energía.
-Tacto: Siente el terreno donde está parado ("Suelo firme" o "Arena movediza") y también la arena
 de las casillas vecinas (norte, sur, este y oeste) antes de pisarla. La arena que siente se guarda en memoria.
-Gusto: Prueba las bayas que encuentra: "Bayas dulces" (+20 de energía) o "Bayas amargas" (-10 de energía).
 Es el sentido con el que el agente aprende: al probar una baya, recuerda si ese color es bueno o malo
 (ver "Aprendizaje de las bayas"). Cuando se come una baya, la olvida de la memoria.

Aprendizaje de las bayas

Al inicio el agente no sabe qué bayas son buenas y cuáles son malas. Aprende de su experiencia:
1. Con la vista solo distingue el color: rojas o azules.
2. Cuando pisa una baya, se la come y el gusto le dice si es dulce (+20) o amarga (-10).
3. Guarda en memoria ese color como "buena" o "mala" y en el estado aparece, por ejemplo,
   "¡Aprendió: bayas azules son malas! (-10)".
4. Desde ese momento aplica lo aprendido a todas las bayas de ese color:
   evita las de color malo y, con poca energía, busca las de color bueno.
5. Nunca vuelve a comer una baya de color malo. Si no hay otro camino y tiene que pasar por encima,
   la deja donde está y en el panel aparece "Gusto: No come bayas azules".

Por eso siempre tiene que comer al menos una baya mala para aprender a evitarlas.
En el mundo actual las rojas son buenas y las azules son malas (ver los sprites en `Recursos/images/`).

Memoria del terreno (`Agente_Cazador/memoria.py`)

Además de las celdas revisadas y la última posición del jaguar, la memoria guarda:
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
2. Si ve al jaguar, lo persigue apuntando a donde va a estar (persecución).
3. Si lo escucha, va hacia la dirección del sonido.
4. Si lo huele, sigue el rastro del olor.
5. Si recuerda dónde lo vio, va hacia donde huyó (2 casillas más adelante en su dirección).
6. Si ya cazó al jaguar, regresa a su cabaña (el campamento). Al llegar recupera su energía,
   se queda ahí y en el estado aparece "En la cabaña: ¡misión cumplida!".
7. Si no percibe nada, explora zonas que todavía no ha revisado.

Después de moverse una casilla, el agente vuelve a usar la vista, el oído y el olfato desde su nueva
posición. Así todo lo que muestra el panel (vista, oído, olfato, tacto y gusto) corresponde a la casilla
donde está parado en ese momento.

Panel de la interfaz

-Fila 1: Energía y estado del agente.
-Fila 2: Vista, Oído (dirección e intensidad) y Memoria (celdas revisadas).
-Fila 3: Tacto, Gusto y Olfato (jaguar o bayas de color bueno).
-Fila 4: Controles, Arena cerca (N, S, E, O) y lo que ha aprendido de las bayas
 ("Rojas: buena  Azules: mala"; "?" si todavía no las prueba).
-Fila 5: Masa y velocidad del cazador, estado y velocidad del jaguar, y pasos (y cuántos fueron repetidos).

En el tablero se marca el alcance de cada sentido alrededor del cazador, con el mismo color que su texto
en el panel. Cada cuadro va un poco más adentro de la casilla para que se vean aunque compartan casillas:
-Vista: amarillo (borde exterior). Las casillas tapadas por árboles no se marcan.
-Oído: gris (en medio).
-Olfato: azul cielo (más adentro).

Requisitos del proyecto

| Requisito                       | Dónde está                                                              |
|---------------------------------|-------------------------------------------------------------------------|
| Memoria                         | `Agente_Cazador/memoria.py`                                             |
| Sentidos                        | `Agente_Cazador/sentidos.py` (vista, oído, olfato, tacto y gusto)       |
| Objetivos                       | `Agente_Cazador/agente.py` (cazar al jaguar, explorar, comer, descansar)  |
| Suelo y costos                  | `Algoritmos/a_Estrella.py`, energía en `agente.py`, rozamiento en `Fisica/` |
| Eficiencia (no repetir nodos)   | Nodos cerrados en A* y costo extra a casillas ya pisadas               |
| Obstáculos                      | Árboles: no se pueden cruzar y tapan la vista                          |
| Persecución                     | `Algoritmos/persecucion.py`                                             |
| Escape                          | `Algoritmos/huida.py` y `Agente_Jaguar/agente.py`                         |
| Masa / física cinemática        | `Fisica/cinematica.py`                                                  |

Objetivos del cazador
-Principal: cazar al jaguar (estar en la misma casilla que él).
-Al terminar: regresar a su cabaña (el campamento) después de cazar al jaguar.
-Sobrevivir: no quedarse sin energía (regresa al campamento o come bayas buenas).
-Explorar: revisar las zonas del mapa que todavía no ha visto.

Suelo y costos
-Pasto: cuesta 2 de energía y 2 en el A*. Rozamiento 0.10.
-Arena movediza: cuesta 8 de energía y 8 en el A*. Rozamiento 0.40 (todos van más lento).
-Bayas malas que ya conoce: costo 20 en el A* para rodearlas.
-Casillas que ya pisó: +2 en el A* para preferir caminos nuevos.

Eficiencia de movimientos (no repetir nodos)
-El A* guarda una lista de nodos cerrados: un nodo que ya expandió no lo vuelve a expandir.
 Se probó contra Dijkstra en 600 caminos y siempre encontró el camino más barato.
-La memoria cuenta cuántas veces pisa cada casilla. Esas casillas cuestan +2 en el A*, así el
 cazador prefiere caminos nuevos.
-Exploración por fronteras: para elegir a dónde explorar, calcula con una sola búsqueda (Dijkstra) el
 costo real de llegar a cada casilla no revisada y le resta cuántas casillas nuevas vería desde ahí.
 Elige la de menor puntaje: cerca, sin repetir camino y que descubra mucho terreno.
-En pruebas (60 mundos) los pasos repetidos bajaron de 32% a 20%. Explorando repite solo 8-10%.
 El resto viene de perseguir al jaguar (que da vueltas) y de regresar al campamento, que casi siempre
 es por donde ya pasó; esas repeticiones no se pueden evitar del todo.
-El panel muestra los pasos y cuántos fueron repetidos.

Persecución y escape
-Cuando el cazador ve al jaguar, usa `persecucion.py` para cortarle el paso ("Cortándole el paso").
-Si lo pierde de vista, sigue 2 casillas más adelante de donde lo vio por última vez, en la
 dirección en que huía ("Siguiendo hacia donde huyó el Jaguar").
-El jaguar huye con `huida.py` cuando el cazador está a 4 casillas o menos.
-Lo atrapa cuando los dos están en la misma casilla.

Masa y física cinemática (`Fisica/cinematica.py`)

Los personajes no saltan de casilla en casilla: aceleran, alcanzan una velocidad y recorren la distancia
(1 casilla = 2 metros). En cada cuadro de animación (60 por segundo):

   F_neta = F_motriz - mu * m * g - b * v
   a = F_neta / m            (segunda ley de Newton)
   v = v + a * dt
   x = x + v * dt

-m: masa. mu: rozamiento del suelo. g: 9.8 m/s². b: coeficiente de arrastre.
-Velocidad máxima: v_max = (F_motriz - mu * m * g) / b
-Al cambiar de dirección pierde la mitad de su velocidad (tiene que frenar para girar).

|           | Masa  | Fuerza | v_max en pasto | v_max en arena |
|-----------|-------|--------|----------------|----------------|
| Cazador   | 75 kg | 400 N  | 2.72 m/s       | 0.88 m/s       |
| Jaguar      | 55 kg | 330 N  | 2.30 m/s       | 0.95 m/s       |

El jaguar es más ligero: acelera más rápido y en arena es más rápido, pero en pasto su velocidad máxima
es menor, por eso el cazador lo puede alcanzar. Cada agente decide su siguiente paso cuando su cuerpo
llega a la casilla, así que cada uno va a su propio ritmo.

Las carpetas `__pycache__` contienen archivos temporales generados automáticamente por Python al ejecutar el programa. 
Estos archivos no forman parte de la lógica principal del proyecto.
