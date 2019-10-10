# Python Edge IoT Framework

## Description

The system based on micro services architecture, and it is:
- event driven design
- platform agnostic

flexibility and resilience

```
EdgeWrapper ==> MicroService:
mode:
    - solo mode (single device no distributed system)
    - network mode (multiple devices, as distributed system)
context: Local Network
Components:
    - software services tree
    - Web server
    - API (end points for every PyService)
    - Dashboard
    - Admin (for every PyService)

EdgeService ==> SoftwareService:
context: Host
Components:
    - API registry to EdgeWrapper (using Flask & Blueprint)
```

### Edge-server
Services manager, provide API, B.O, WebUI, admin, dashboard.

### Device-service
Sensor data is collected by a Device Service from a thing, and published in Mqtt-service.

Device-service provide API

### Mqtt-service
The MQTT protocol provides a lightweight method of carrying out messaging using a publish/subscribe

## Config

Configure device machine type by env var:

`EDGE_MACHINE_TYPE=pc_linux`

Docker base image by machine types

`balenalib/raspberrypi3-python:3`

`balenalib/raspberrypi3-debian:jessie`

`balenalib/raspberrypi3-debian:stretch-run-20190612`

## Machine types

x86:
- pc_linux
- pc_win
- mac

ARM:
- rpi

## Architecture

La clé se n'est pas le code, mais l'architecture

```
CustomProject
    /-- PyEdgeIoTFramework
    /-- CustomService
    docker-compose.yml
```

## Docker-compose

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
## Script shell

Commands:
- ls: pour lister les fichiers du répertoire.
- cd: pour changer de répertoire.
- mkdir: pour créer un répertoire.
- grep: pour rechercher un mot.
- sort: pour trier des mots.

## ToDo
- ToDo: Add PySse service (like mqtt)
- ToDo: Add PyMplayer service (like omxplayer)