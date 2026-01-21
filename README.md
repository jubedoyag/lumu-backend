# Backend Test Lumu 2026

Proyecto en Python y FastAPI para exponer servicios de publicación y subscripción a un *topic*
en Kafka.

La siguiente guía está diseñada para ser ejecutada en un entorno Linux usando la terminal.


## Prerrequisitos para ejecución

* Tener Docker instalado -> [Get Docker](https://docs.docker.com/get-started/get-docker/)
* Descargar el repositorio -> https://github.com/jubedoyag/lumu-backend
* Una vez descargado el repositorio, ubicarse en el directorio `part2/`


## Como ejecutarlo

Se puede ejecutar fácilmente el proyecto ejecutando Docker Compose:

```bash
sudo docker compose up
```
**Nota**: Este comando ocupará la terminal y mostrará los *logs* relacionados a cada
servicio. Para llevar la ejecución del proyecto a segundo plano, la opción `-d` al final
del comando bastará.

Una vez todos los contenedores se ejecuten con normalidad se pueden probar los servicios
del productor de mensajes y del consumidor de la siguiente forma:

### Consumidor

* Dirigirse al enlace http://127.0.0.1:8000/is-node-active para verificar correcto funcionamiento.
Si el servicio inició correctamente debería mostrar un JSON con un *status* en `true` y un UUID
que identifica el nodo de consumo en la red interna de Docker.
* En el enlace http://127.0.0.1:8000/number-ips se puede consultar el número de IPs que el nodo
ha extraído de cada mensaje consumido del *topic* de Kafka. Antes de iniciar el proceso de
producción de mensajes, el conteo será 0. Una vez iniciada la producción, se podrá recargar la
página y ver como aumenta el contador.
* En el enlace http://127.0.0.1:8000/global-number-ips se puede consultar el conteo global de IPs 
que el nodo ha calculado mediante un proceso de votación con los nodos a los cuales se conectó.

Una vez se hara iniciado con la producción de mensajes, el mensaje debe verse similar a algo así:

```
{"number":11,"voted_by":1,"voting_nodes":2,"votes":{"10":1, "11":1}}
```


### Productor
* Dirigirse al enlace http://127.0.0.1:7000/ para verificar correcto funcionamiento.
Si el contenedor se está ejecutando bien se debería mostrar el JSON `{"message":"hola mundo"}`

* Para iniciar el envío de mensajes, dirigirse al enlace http://127.0.0.1:7000/start , donde
el mensaje `{"started": true}` saldrá una vez empiece el envío.
El *endpoint* `/start` recibe parámetros en el URL de la petición para cambiar el comportamiento del
envío de mensajes:
    * `num_devices`: De tipo entero, recibe el número de direcciones IPv4 a crear representando cada
    dispositivo que envía mensajes.
    * `num_messages`: De tipo entero, recibe el número de mensajes totales a enviar, alternando
    aleatoriamente cada dispositivo creado previamente.
    * `pause_ms`: De tipo entero, recibe el tiempo en milisegundos que pasará entre cada envío de
    mensaje.

**Ejemplo**: http://127.0.0.1:7000/start?num_devices=100&num_messages=1000&pause_ms=100

En este punto es posible ver los *logs* del servicio `producer` que imprimirá cada mensaje enviado.


## Iniciar contenedores individualmente

Si se desea ejecutar manualmente cada contenedor (por ejemplo, para poder ejecutar más servicios
de consumo) es posible realizarlo de la forma tradicional en Docker, primero construyendo las
imágenes y luego ejecutando cada contenedor.

**Nota**: Todos los contenedores harán parte de una misma red interna para facilitar su
comunicación. Para crear dicha red podemos usar el siguiente comando:
```bash
sudo docker network create --subnet 10.0.0.0/24 --driver=bridge example-net
```

Primero podemos ejecutar el contenedor de Kafka, el cual no requiere construir su imagen sino solo
descargarla. El siguiente comando permite realizar este paso:

```bash
sudo docker run -d \
    --name kafka -p 9092:9092 \
    -e KAFKA_NODE_ID=1 \
    -e KAFKA_PROCESS_ROLES=broker,controller \
    -e KAFKA_LISTENERS="PLAINTEXT://:9092,CONTROLLER://:9093" \
    -e KAFKA_ADVERTISED_LISTENERS="PLAINTEXT://kafka:9092" \
    -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER \
    -e KAFKA_CONTROLLER_QUORUM_VOTERS="1@kafka:9093" \
    -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
    --network example-net apache/kafka:latest
```

Como Kafka requiere de un *topic* en el cual los productores publican y al cual los consumidores se
suscriben, antes de iniciar con los otros servicios se debe iniciar el *topic*, lo cual se puede
realizar ejecutando un *script* en Kafka con los siguientes comandos:
1. Ingresar al servicio de Kafka: `sudo docker exec -it --workdir /opt/kafka/bin kafka bash`
2. Ejecutar el comando: `.kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test-topic`


**Nota 2**: Los servicios de producción y consumo de mensajes requieren de variables de entorno,
para ello se puede crear un archivo `container.env` que se encuentre en el directorio
`part2/consumer/backend/` (de forma análoga para el servicio `producer`) que tenga el siguiente
contenido:

```bash
KAFKA_SERVER=kafka:9092
KAFKA_TOPIC=test-topic
NODES_NETWORK=10.0.0.0/24
DISCOVERING_INTERVAL=10
```

Para construir la imagen del servicio `consumer` debemos ubicarnos en el directorio
`part2/consumer/backend/` y ejecutar el siguiente comando:

```bash
sudo docker build -t lumu-consumer .
```

El proceso para construir la imagen del servicio `producer` es equivalente.


Ahora, para ejecutar el servicio de producción de mensajes, podemos usar el siguiente comando:

```bash
sudo docker run -d -p 7000:7000 \
    --name producer \
    --network example-net \
    --env-file ./container.env lumu-producer
```

Para ejecutar el servicio de consumo de mensajes, podemos usar el siguiente comando:

```bash
sudo docker run -d -p 8000:8000 \
    --name consumer1 \
    --network example-net \
    --env-file ./container.env lumu-consumer
```

Si ya se cuenta con un primer nodo de consumo, se pueden crear más cambiando el puerto expuesto
del *host* y el nombre del contenedor:

```bash
sudo docker run -d -p 8001:8000 \
    --name consumer2 \
    --network example-net \
    --env-file ./container.env lumu-consumer
```

