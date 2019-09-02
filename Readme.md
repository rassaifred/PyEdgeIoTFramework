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
Configure service type by env var:

`EDGE_SERVICE=n_service`

## Custom services

```
custom-service
    folder: CustomService

```