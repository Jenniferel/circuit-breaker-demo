# Circuit Breaker Demo

![Diagrama Circuit Breaker](https://miro.medium.com/max/1400/1*5sJSP6yJkZk6LRWyb5zqOg.png)

Demo interactivo que muestra el patrón Circuit Breaker implementado entre dos microservicios usando Docker.

## Estructura del Proyecto

circuit-breaker-demo/

├── service-a/ # Servicio cliente con Circuit Breaker

│ ├── app.py # Aplicación Flask con interfaz web

│ ├── Dockerfile # Configuración Docker para Service A

│ └── requirements.txt # Dependencias Python

├── service-b/ # Servicio simulado con fallos controlables

│ ├── app.py # Lógica del servicio con modos de fallo

│ ├── Dockerfile # Configuración Docker para Service B

│ └── requirements.txt # Dependencias Python

└── docker-compose.yml # Orquestación de contenedores
