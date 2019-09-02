# Description
The system based on micro services architecture, and it is:
- event driven design
- platform agnostic

## Edge-server
Services manager, provide API, B.O, WebUI, admin, dashboard.

## Device-service
Sensor data is collected by a Device Service from a thing, and published in Mqtt-service.

Device-service provide API

## Mqtt-service
The MQTT protocol provides a lightweight method of carrying out messaging using a publish/subscribe

# Architecture

```
CustomProject
    /-- PyEdgeIoTFramework
    /-- CustomService
    docker-compose.yml
```

# Docker-compose

## Edge services

```
edge-server
    folder: PyEdgeIoTFramework
    env_avr: server
device-service
    folder: PyEdgeIoTFramework
    env_avr: device
mqtt-service
    image: mosquitto
```

## Custom services

```
custom-service
    folder: CustomService

```

# Config

Configure service type by env var:

`EDGE_SERVICE=n_service`

the service start with line from DockerFile:

`CMD ["bash", "/bin/start_edge.sh"]`
in start_edge.sh
```
run_server () {
    /usr/bin/python /server.py
}

run_device () {
    /usr/bin/python /device.py
}

if [[ "EDGE_SERVICE" = "server" ]]; then
    run_server
    
if [[ "EDGE_SERVICE" = "device" ]]; then
    run_device
    
```