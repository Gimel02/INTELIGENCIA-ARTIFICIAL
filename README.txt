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

Ratones: agente continuo (`Agente_Raton/agente.py`)

A diferencia del cazador y del jaguar, los ratones NO se mueven de casilla en casilla: su posición es
continua (con decimales) y tienen un vector de velocidad. En cada cuadro de animación:
-Merodean: cambian poco a poco de dirección al azar (0.5 casillas/s).
-Huyen: si perciben al jaguar a 3 casillas o menos, corren en dirección contraria (0.95 casillas/s).
-Evitan obstáculos: miran un poco hacia adelante y giran si hay un árbol o el borde del mapa.
-Aceleran poco a poco hacia la velocidad que quieren (no cambian de velocidad de golpe).
Hay 3 ratones. El jaguar se come un ratón cuando lo alcanza (a menos de 0.6 casillas).

Jaguar: agente inteligente (`Agente_Jaguar/agente.py`)

El jaguar tiene hambre, que sube con cada decisión: NORMAL (< 40), HAMBRIENTO (40-79) y
HAMBRE INDOMABLE (80-100). Decide en este orden:
0. Si acaba de atacar al cazador, se retira huyendo durante 6 decisiones.
1. Inversión de papeles: ataca al cazador (lo persigue con `persecucion.py`) si el cazador está débil
   (energía < 30) o si tiene HAMBRE INDOMABLE y ya no quedan ratones.
2. Si detecta al cazador a 4 casillas o menos, huye con `huida.py` (o queda "Acorralado").
3. Si tiene hambre (40 o más), caza al ratón más cercano que huela (6 casillas). Si no huele ninguno,
   sale a buscarlos.
4. Si no, descansa o merodea.
Comer un ratón le quita 50 de hambre.

Encuentro cazador - jaguar
-Si el jaguar está atacando: el cazador pierde 30 de energía y 1 de sus 3 vidas, y el jaguar se retira.
 Sin vidas, el cazador queda vencido.
-Si no: el cazador atrapa al jaguar.
-Mientras el jaguar ataca, y justo después del ataque (hasta su primer paso de huida), el cazador no lo
 puede atrapar. Ya huyendo, si el cazador lo alcanza, lo atrapa.
El panel muestra las vidas del cazador junto a la energía y el hambre del jaguar junto a su estado.

Evitar ir y volver entre dos casillas (algoritmo genético + A*)
-El AG planea 20 movimientos, pero el cazador solo ejecuta el primero. Por eso, un plan cuyo primer
 movimiento choca (árbol, borde o baya mala conocida) recibe un castigo de -1 en la aptitud.
-El AG trata las bayas malas que el cazador conoce como obstáculos (parámetro `prohibidas`).
-El cazador solo acepta el paso del AG si de verdad lo acerca a la meta (costo real calculado con
 `costos_desde`). Si no, usa el paso del A*.
-Al perseguir, si la presa está a 2 casillas o menos va directo hacia ella, sin adelantarse
 (si la presa huye en zigzag, adelantarse lo haría ir de un lado a otro).
En pruebas (30 mundos) las idas y vueltas (A -> B -> A -> B) bajaron de 120 a 17.

Métodos de selección y cruce del algoritmo genético (`Algoritmos/genetico.py`)

Al inicio del archivo hay una configuración para elegir cómo evoluciona la población:

-METODO_SELECCION: cómo se escogen los padres.
 "elitismo": dos padres al azar entre los 4 mejores.
 "ruleta": cada individuo tiene un pedazo de la ruleta según su lugar (escalamiento por rango: el peor
           vale 1 y el mejor vale N). Los mejores tienen más probabilidad, pero cualquiera puede ser padre.
 "torneo": se escogen 3 individuos al azar y gana el de mejor aptitud.
-PROPORCION_CRUCE: probabilidad de que dos padres se crucen (crossover rate). Si no se cruzan, los
 hijos son copias de los padres (y solo cambian por mutación).
-PUNTO_CRUCE_ALEATORIO: True = el punto de cruce se elige al azar; False = siempre a la mitad.
-TAMANO_TORNEO: cuántos individuos compiten en cada torneo.
En todos los métodos los 2 mejores individuos (élite) pasan directo a la siguiente generación,
y la mutación es de 10% por gen.

Comparación de métodos (120 mundos por método, hasta 4 minutos cada uno):

| Método                                   | Jaguar cazado | Cazador agotado | Idas y vueltas* |
|------------------------------------------|---------------|-----------------|-----------------|
| Elitismo, cruce 100%, punto a la mitad   | 65%           | 28%             | 3.8             |
| Elitismo, cruce 70%, punto al azar       | 69%           | 24%             | 4.6             |
| Ruleta, cruce 70%, punto al azar         | 66%           | 22%             | 5.7             |
| Torneo, cruce 70%, punto al azar         | 64%           | 27%             | 5.6             |
*por cada 1000 pasos

Las diferencias son pequeñas (dentro de lo que cambia por azar entre mundos). Se dejó como
predeterminado elitismo con cruce de 70% y punto al azar, que tuvo el mejor resultado.

También se probó el AG solo (sin la revisión con A*) en 400 caminos de 8 a 18 casillas rodeando
árboles, con 10 individuos y 20 generaciones: llegó a la meta en 29-34% de los casos según el método.
Por eso el cazador revisa cada paso del AG y usa el A* si el paso no lo acerca a la meta.

Autoconciencia del cazador (`Agente_Cazador/agente.py`)

`tomar_decision()` envuelve la decisión original (`decidir_y_actuar()`). En cada turno el cazador:

1. Es consciente de sus sentidos: arma un resumen de lo que percibe con cada sentido
   (`resumen_sentidos()`) y sabe qué sentido o motivo causó su decisión (`sentido_de_la_decision()`):
   vista, oído, olfato, memoria o energía.
2. Es consciente de su cuerpo (peso): conoce su cuerpo físico (`self.cuerpo`): masa (75 kg), fuerza
   (400 N), velocidad actual y velocidad máxima en pasto y en arena (`conciencia_fisica()`). Con eso
   estima cuánto tardaría en recorrer un camino (`tiempo_estimado()`, `tiempo_a_la_cabana()`).
3. Es consciente de sus acciones: guarda una bitácora con sus últimas 40 decisiones: turno, de dónde a
   dónde, acción (ARRIBA, ABAJO, IZQUIERDA, DERECHA o QUIETO), meta, motivo, sentido usado, quién
   decidió el paso (AG, A* o ataque directo), resultado y energía antes y después.
4. Detecta problemas al decidir y reacciona (`detectar_problema()`, `reaccionar_a_problema()`):

| Problema       | Cómo lo detecta                                   | Qué hace                                  |
|----------------|---------------------------------------------------|-------------------------------------------|
| Sin ruta       | El A* no encuentra camino a su meta               | Descarta esa meta 15 turnos y busca otra  |
| Bloqueado      | No pudo dar el paso                               | Descarta esa meta 15 turnos y busca otra  |
| Atascado       | 6 turnos sin moverse (sin haber terminado)        | Cambia de zona de búsqueda                |
| Dando vueltas  | A -> B -> A -> B con la MISMA meta                | Descarta esa meta y busca otra            |

-Si la meta es una casilla prohibida (baya mala o meta descartada), va a la casilla vecina alcanzable
 más cercana. Por ejemplo, si el jaguar está parado sobre una baya mala, lo acecha desde al lado.
-La persecución también evita apuntar a casillas prohibidas.
-En pruebas (120 mundos), sin las reacciones hubo 675 decisiones "sin ruta" (el punto donde quería
 interceptar al jaguar estaba encerrado por árboles); con las reacciones solo hubo 1.

En el panel: "Cazador 75 kg, 1.5 m/s" (su cuerpo) y "Usó: vista | ARRIBA (AG)" (sentido, acción y quién
la decidió). Si hay un problema, esa línea cambia a rojo: "PROBLEMA: sin ruta (reaccionando)".
Tecla B: imprime en la terminal su autoconciencia completa (sentidos, cuerpo, energía, problema actual,
metas descartadas y las últimas 10 decisiones de la bitácora).

Entorno dinámico: Percepción -> AG -> Acción

El jaguar es el ENEMIGO: se mueve, caza ratones, huye y puede atacar al cazador. En cada turno:

   PERCEPCIÓN                         AG (algoritmo genético)              ACCIÓN
   vista, oído, olfato,      --->     cromosoma = 20 acciones      --->   el cazador ejecuta
   tacto, gusto, memoria              (ARRIBA, ABAJO, IZQUIERDA,          el primer movimiento
   (¿dónde está el jaguar?            DERECHA). Aptitud: acercarse        del mejor cromosoma
   ¿está atacando?)                   a la meta, sin chocar y, si el
                                      jaguar ataca, sin pasar junto a él

-Percepción -> AG: si el cazador percibe al jaguar con cualquier sentido, el AG recibe su posición
 (`enemigo`). Si el jaguar lo está atacando (`evitar_enemigo`), cada paso del plan que quede junto al
 jaguar resta 0.5 de aptitud.
-Si el jaguar lo ataca y está a 3 casillas o menos, el cazador huye usando `Algoritmos/huida.py`
 (el mismo algoritmo de huida del jaguar), sin pasar por bayas malas.

Premios y castigos (en el juego, no solo en el AG)

Como en otros proyectos, el premio es más batería (energía) y el castigo es perderla:

| Situación                                           | Batería | Puntos |
|-----------------------------------------------------|---------|--------|
| Buena decisión del AG (paso válido que lo acerca)    | +1      | +1     |
| El AG propone chocar con un obstáculo                 | -2      | -2     |
| Cazar al jaguar                                      | +30     | +50    |
| Ser atacado por el jaguar                            | -30     | -10    |
| Comer baya buena / baya mala                          | +20/-10 | -      |

Dentro del AG también hay premios y castigos en la aptitud: premio por acercarse a la meta y por el
progreso del primer paso; castigo por chocar (más fuerte si el primer paso choca), por pisar arena,
por repetir casillas y por pasar junto al enemigo cuando ataca.

Los puntos se ven en el panel ("Puntos: N") y cada premio o castigo queda en la bitácora (tecla B).

En pruebas (120 mundos): sin premios el cazador cazó al jaguar en 69% y se agotó en 27%; con premios
cazó en 88% y se agotó en 10%. Los choques del AG casi no ocurren (0-1 en 120 mundos) porque la
aptitud ya castiga mucho que el primer paso choque.

Las carpetas `__pycache__` contienen archivos temporales generados automáticamente por Python al ejecutar el programa. 
Estos archivos no forman parte de la lógica principal del proyecto.


Control difuso (Mamdani): quién toma las decisiones

DIOS (Logica_Difusa/dios.py) coordina a los agentes:
-Agente 1 = CAZADOR: control difuso, reglas entrenadas con AG.
-Agente 2 = JAGUAR: control difuso, reglas entrenadas con AG.
-Agente Tonto = RATONES: reglas fijas (huir del jaguar o caminar al azar), sin memoria y sin aprender.

En cada turno, el controlador difuso decide QUÉ hace el agente. Después, el AG del movimiento
(o A*) decide CÓMO llega el cazador a su meta.

   CAZADOR                                                  JAGUAR
   entradas: reserva (0-100), distancia (0-30),             entradas: hambre (0-100),
             peligro (0-100)                                          distancia_cazador (0-30),
   salida:   huir | recargar | explorar | perseguir |                 energia_cazador (0-100)
             atacar                                         salida:   huir | merodear |
   23 reglas                                                          cazar_raton | atacar
                                                            11 reglas

   Input -> Fuzzificación (grados 0-1) -> Inferencia (IF-THEN, AND=min, OR=max, NOT=1-x,
   implicación=min, AGG=max) -> Centroide (x* = Σxμ/Σμ) -> Output

-reserva = energía - energía para volver al campamento.
-distancia = casillas hasta el jaguar (o hasta donde lo vio). 30 si no sabe nada de él.
-peligro = 100 si el jaguar lo ataca, el hambre del jaguar si lo percibe, 0 si no lo percibe.

Archivos (carpeta Logica_Difusa/):
-funciones_membresia.py: grado, grado inversa, triangular y trapezoidal.
-operadores.py: AND, OR, NOT, implicación y AGG.
-variables.py: variables lingüísticas y sus puntos X0..X3.
-base_conocimiento.py: reglas IF-THEN, guardar/cargar en JSON, cromosoma <-> reglas.
-motor_mamdani.py: fuzzificación, inferencia y centroide.
-dios.py: orquestador DIOS.
-simulador.py: partidas sin ventana para entrenar y comparar.
-entrenamiento_genetico.py: el AG que crea las reglas.
-comparar.py: compara reglas entrenadas, del equipo y al azar.
-bases/: la base de conocimiento (memoria) de cada agente en JSON.
-reporte/: reporte y gráficas.

Comandos:
   python3 -m Logica_Difusa.entrenamiento_genetico jaguar      (entrena al jaguar)
   python3 -m Logica_Difusa.entrenamiento_genetico cazador     (entrena al cazador)
   python3 -m Logica_Difusa.comparar 60                        (compara en 60 mapas nuevos)

En la ventana, la tecla D cambia entre las reglas entrenadas y las del equipo, y reinicia la
partida. La bitácora (tecla B) muestra la decisión difusa del cazador en cada turno: x*, la acción
y las reglas que más pesaron.


Qué cambió en los archivos que ya existían (explicado para el equipo)

Antes, el cazador y el jaguar decidían con una cadena de "if": si pasa esto, haz aquello.
Ahora, en cada turno, le preguntan al sistema difuso qué hacer. El sistema difuso NO mueve al
agente: solo dice la ACCIÓN. Después, el código que ya teníamos (AG del movimiento, A*, huida,
etc.) se encarga de dar el paso.

   El agente mide sus entradas  ->  el sistema difuso responde una acción  ->  el agente
   elige su meta según esa acción  ->  el AG del movimiento o A* da el paso


1. Agente_Cazador/agente.py (el que más cambió)

   ANTES: decidía con una "reserva de seguridad" fija y una variable "en_peligro". Si su
   energía bajaba de cierto número, regresaba; si veía al jaguar cerca, huía. Era todo o nada.

   AHORA:
   -Se agregó la función entradas_difusas(). Calcula los 3 datos que el cazador le da al
    sistema difuso:
       reserva   = energía que le queda - energía que necesita para volver al campamento
       distancia = casillas hasta el jaguar (o hasta donde lo vio la última vez); 30 si no
                   sabe nada de él
       peligro   = 100 si el jaguar lo está atacando, el hambre del jaguar si lo ve, 0 si no
                   lo ve
   -Se agregó la función decidir_difuso(). Le manda esos 3 datos al controlador difuso y
    recibe una de estas 5 acciones:
       huir       -> se aleja del jaguar (usa la huida que ya existía)
       recargar   -> modo supervivencia: va por bayas buenas o regresa al campamento
       explorar   -> sigue explorando el mapa como antes
       perseguir  -> calcula dónde cortarle el paso al jaguar y va hacia ahí
       atacar     -> va directo a la casilla del jaguar
   -En decidir_y_actuar() se reemplazó el bloque viejo de reserva_seguridad / en_peligro por
    esas 5 acciones. Lo demás (memoria, bayas, mapa, AG del movimiento) sigue igual.
   -Antes, si el jaguar estaba en la casilla de al lado, el cazador lo atacaba siempre. Ahora
    solo lo hace si su decisión difusa fue perseguir o atacar.
   -La bitácora (tecla B) ahora también muestra la decisión difusa. Ejemplo:
       x*=33.3 recargar | R21->huir (0.67)
    Quiere decir que el centroide dio 33.3, la acción fue recargar y la regla que más pesó
    fue la R21 con fuerza 0.67.

2. Agente_Jaguar/agente.py

   ANTES: decidía con "if" sobre su hambre y la distancia al cazador.

   AHORA: le da al sistema difuso estos 3 datos:
       hambre             = qué tanta hambre tiene (0 a 100)
       distancia_cazador  = casillas hasta el cazador
       energia_cazador    = energía del cazador (si está débil, el jaguar se anima a atacar)
   y recibe una de estas 4 acciones:
       atacar       -> calcula dónde interceptar al cazador y va hacia ahí con A*
       huir         -> busca la mejor ruta de escape; si está acorralado y el cazador está a 2
                       casillas o menos, contraataca
       cazar_raton  -> va por el ratón más cercano que pueda oler (6 casillas o menos); si no
                       hay ninguno, camina buscando
       merodear     -> descansa o camina por la selva
   -Lo que NO cambió: después de atacar, el jaguar se retira unos turnos sin preguntarle al
    sistema difuso (igual que antes).
   -Ahora guarda su hambre en mundo.hambre_jaguar para que el cazador la pueda usar como
    "peligro" cuando lo ve.

3. Agente_Raton/agente.py

   No cambió su comportamiento. Solo se agregó un comentario arriba que dice que los ratones
   son el AGENTE TONTO: siguen reglas fijas (si ven al jaguar huyen, si no caminan al azar),
   no tienen base de conocimiento y no aprenden.

4. Interfaz/interfaz.py

   -El panel de abajo ahora muestra la decisión difusa, por ejemplo:
       ... | difuso (entrenadas): perseguir
   -Se agregó la tecla D. Cambia entre las reglas entrenadas por el AG y las reglas que
    hicimos a mano (equipo), y reinicia la partida. Sirve para comparar en vivo cómo se
    comporta cada una.

5. README.txt

   Se agregó esta sección y la de arriba.


Lo que NO se tocó: Mundo/, Algoritmos/genetico.py (el AG del movimiento), main.py y el resto
de archivos siguen igual.


Ejemplo de un turno del cazador (paso a paso)

   1. El cazador mide: reserva = 30, distancia al jaguar = 4, peligro = 70.
   2. Fuzzificación (qué tanto pertenece cada dato a cada palabra, de 0 a 1):
         reserva 30   -> baja 0.5, media 0.5
         distancia 4  -> cerca 0.67, media 0.33
         peligro 70   -> tranquilo 0.25, agresivo 0.75
   3. Reglas: se evalúan las 23 reglas con AND=min, OR=max, NOT=1-x. Por ejemplo:
         R21: SI peligro es agresivo Y distancia es (muy_cerca O cerca) ENTONCES huir
              = min(0.75, max(0, 0.67)) = 0.67
   4. Cada acción se recorta a la fuerza de sus reglas (huir 0.67, recargar 0.33,
      perseguir 0.25) y se juntan con max.
   5. Centroide: el punto de equilibrio de esa figura da x* = 33.3, que cae en "recargar".
   6. El cazador entra en modo supervivencia y el AG del movimiento le da el paso.


Cómo ver o cambiar las reglas

   Las reglas de cada agente están en Logica_Difusa/bases/ en archivos JSON:
       cazador_entrenadas.json, jaguar_entrenadas.json  -> las que encontró el AG
       cazador_equipo.json, jaguar_equipo.json          -> las que hicimos a mano
   Cada regla se ve así:
       "id": "R01",
       "si": { "y": [ reserva es muy_baja, distancia es muy_cerca, NO peligro es agresivo ] },
       "entonces": ["accion", "explorar"]
   Para cambiar lo que hace una regla, se cambia la acción de "entonces" (por ejemplo,
   "explorar" por "huir") y se vuelve a correr el juego. Si se vuelve a entrenar con el AG,
   el archivo *_entrenadas.json se sobrescribe.

Para entender todo con más detalle (gráficas, ejemplo con números y resultados del
entrenamiento), ver Logica_Difusa/reporte/REPORTE_CONTROL_DIFUSO.md.
