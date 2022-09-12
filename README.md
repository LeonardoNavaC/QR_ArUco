# QR_ArUco

El algortimo imlementado esta basado en la navegación a un punto usando un controlador P, para ambas velocidades angular y lineal. Realizando el bonus de la actividad propuesta para el challenge de "Autonomous Navigation" para Quantum Robotics.

Al estar utilizando ROS, es imprtante mencionar algunos conceptos básicos de este sistema operativo, los cuales son tópicos y nodos. El programa de python adjunto en QR_ArUco/QR/src/autonomous_navigation_qr/src llamado ArUco_autonomous.py, es el encargado de funcionar como nodo, este recibira los datos proporcionados. Los tópicos son canales por los cuales se comunican estos nodos.

El programa inicia importando algunas librerias para poder hacer funcional el challenge, posteriormente se crea una clase la cual representa al "Rover", asignandole atributos como a que tópico se suscribe con su tipo de dato (turtle1/pose) y a que tópico publicará (turtle1/cmd_vel). Ademas se inicializan los métodos necesarios para poder ejecutar el algoritmo, como "move()" que recibe las velocidades lineal y angular y las publica en el tópico "turtle1/cmd_vel"; o "create_reference_points()", el cual, dado el punto de llegada final crea 8 puntos al rededor para que el robot pueda buscar el código. 

Para poder seguir con la explicación, es importante mencionar dos aspectos; el primero es que se usará un controlador P para ambas velocidades; el segundo punto va relacionado a este controlador, ya que este programa se estara ejecutando con una frecuencua de 20 Hz (ya que así es definido en el programa), este algoritmo de control será ejecutado esa misma cantidad de veces por segundo.

El algoritmo inicia si es llamado de forma principal y no importado a otro archivo. Se declara una instancia de la clase "Rover", con la cual se podrán aplicar todos los métodos anteriormente mencionados. La ejecución principal esta basada en una máquina de estados, la cual cambiará entre: "pointingTowardsGoal", "travelingTowardsGoal" y "goalReached". Cada estado tiene su acción de control respectiva. "pointingTowardsGoal" orienta de en dirección hacia la meta a la simulación del Turtlesim, es decir unicamente se aplica un control proporcional a la velocidad angular (girando sobre su propio eje). "travelingTowardsGoal" viaja en direccion a la meta, sin embargo en este estado se mantiene el control de velocidad angular ademas de añadir el control de velocidad lineal, esto de que en caso de ser implementado en un agente físico, se puedan contrarrestar errores de la pista o de los motores. Finalmente "goalReached" es el estado donde aproximadamente se llega a la meta, y en este se envia una velocidad lineal y angular igual a cero para que el robot no siga avanzando; en este estado, se ejecuta el método "create_reference_points()", ya que se esta proximo a la meta. En todo momento se esta imprimiento en pantalla la posición actual y la posición objetivo.

El algoritmo de control implementado se realiza calculando errores de ángulo y posición, con esto se define la velocidad a la quedebe ir el Rover con la siguiente ecuación

w = Kpw*e_theta

v = Kpv*e_pos

Donde w es la velocidad angular a mandar, v es la velocidad lineal a mandar, Kpw y Kpv son las constantes de proporcionalidad y e_theta y e_pos son los errores de ángulo y posición, el primero calculado con el arcotangente del angulo formado entre la posición actual y la posición de meta, restandose al ángulo actual. el segundo calculado con la distancia euclideana entre dos puntos, el actual y el de referencia. 
