# QR_ArUco

El algortimo imlementado esta basado en la navegación a un punto usando un controlador P, para ambas velocidades angular y lineal. Realizando el bonus de la actividad propuesta para el challenge de "Autonomous Navigation" para Quantum Robotics.

Al estar utilizando ROS, es imprtante mencionar algunos conceptos básicos de este sistema operativo, los cuales son tópicos y nodos. El programa de python adjunto en QR_ArUco/QR/src/autonomous_navigation_qr/src llamado ArUco_autonomous.py, es el encargado de funcionar como nodo, este recibira los datos proporcionados. Los tópicos son canales por los cuales se comunican estos nodos.

El programa inicia importando algunas librerias para poder hacer funcional el challenge, posteriormente se crea una clase la cual representa al "Rover", asignandole atributos como a que tópico se suscribe con su tipo de dato (turtle1/pose) y a que tópico publicará (turtle1/cmd_vel). Ademas se inicializan los métodos necesarios para poder ejecutar el algoritmo, como "move()" que recibe las velocidades lineal y angular y las publica en el tópico "turtle1/cmd_vel"; o "create_reference_points()", el cual, dado el punto de llegada final crea 8 puntos al rededor para que el robot pueda buscar el código. 
