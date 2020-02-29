"""
ToDo: ok - add scan ip's
ToDo: ok - verify if camfi-adress
ToDo: ok - get camfi infos
ToDO: ok - get camera config
ToDo: add socket client camfi
ToDO: add socket event handler
"""

import os
import socket
import multiprocessing
import subprocess
import pycurl
from io import BytesIO
import requests


from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLR import PyDSLR


class PyCamFiMatrix(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.cafmi_list = []
        self.camfi_tool = CamFiTool()
        # ----

    def run(self) -> None:
        # ----
        super().run()
        # ----
        self.cafmi_list = self.camfi_tool.scan_camfi()
        # ----
        # print(cafmi_list)
        # ----
        for c_ip in self.cafmi_list:
            camfi = PyCamFi()
            camfi.ip_adress = c_ip
            camfi.start()


class PyCamFi(EdgeService):

    ip_adress = "0.0.0.0"
    version = "0"
    serial = "0"
    used = .0

    SSID = "-"
    mac = "-"
    network_mode = "-"

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.camera = PyDSLR()
        # ----

    def run(self):
        # ----
        super().run()
        # ----
        print("camfi added with ip adress: {} infos: {}".format(self.ip_adress, self.get_info()))
        # ----
        # get camera config
        # ----
        data = self.get_config()
        if data:
            # x.main.children.status.children.cameramodel.value
            self.camera.cameramodel = data["main"]["children"]["status"]["children"]["cameramodel"]["value"]
            self.camera.deviceversion = data["main"]["children"]["status"]["children"]["deviceversion"]["value"]
            self.camera.eosserialnumber = data["main"]["children"]["status"]["children"]["eosserialnumber"]["value"]
            self.camera.serialnumber = data["main"]["children"]["status"]["children"]["serialnumber"]["value"]
        # ----


    def get_info(self):
        get_url = "{}{}{}".format(REST_API_CAMFI_PROTOCOL, self.ip_adress, REST_API_CAMFI_GET_INFO)
        r = requests.get(get_url)
        return r.json()

    def get_config(self):
        get_url = "{}{}{}".format(REST_API_CAMFI_PROTOCOL, self.ip_adress, REST_API_CAMFI_GET_CONFIG)
        r = requests.get(get_url)
        return r.json()


class CamFiTool:

    def scan_camfi(self):
        # print('Mapping...')
        return map_network()

    def get_camera_info_serial(self):
        pass


def pinger(job_q, results_q):

    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            # print("start ping adress {}".format(ip))
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def map_network(pool_size=4): # (pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # compose a base like 192.168.1.xxx
    base_ip = "192" + '.' + "168" + '.9.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(66, 70): # range(1, 256):
        jobs.put(base_ip + '{0}'.format(i))

    for p in pool:
        jobs.put(None)

    for p in pool:
        p.join()

    # collect he results
    while not results.empty():
        ip = results.get()
        # ip_list.append(ip)
        # ----
        # creates a new socket using the given address family.
        socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # setting up the default timeout in seconds for new socket object
        socket.setdefaulttimeout(.3)

        # returns 0 if connection succeeds else raises error
        result = socket_obj.connect_ex((ip, SOCKET_CAMFI_PORT))  # address and port in the tuple format

        # print(ip, "-", result)

        # closes te object
        socket_obj.close()

        if result == 0:

            url_str = "{}{}{}".format(REST_API_CAMFI_PROTOCOL, ip, REST_API_CAMFI_GET_INFO)

            # print(url_str)

            #
            b_obj = BytesIO()
            crl = pycurl.Curl()

            # Set URL value
            crl.setopt(crl.URL, url_str)

            # Write bytes that are utf-8 encoded
            crl.setopt(crl.WRITEDATA, b_obj)

            # Perform a file transfer
            crl.perform()

            # End curl session
            crl.close()

            # Get the content stored in the BytesIO object (in byte characters)
            get_body = b_obj.getvalue()

            # Decode the bytes stored in get_body to HTML and print the result
            # print('Output of GET request:\n%s' % get_body.decode('utf8'))

            if get_body:
                #
                ip_list.append(ip)

    return ip_list


# ----------------------------------------------------
#            SOCKET EVENTS
# ----------------------------------------------------

SOCKET_CAMFI_PORT = 8080
SOCKET_CAMFI_EVENT_CAMERA_REMOVE = "camera_remove"
SOCKET_CAMFI_EVENT_CAMERA_ADD = "camera_add"
SOCKET_CAMFI_EVENT_TAKEPIC = "takepic"
SOCKET_CAMFI_EVENT_FILE_ADDED = "file_added"
SOCKET_CAMFI_EVENT_LIVESHOW_ERROR = "liveshow_error"
SOCKET_CAMFI_EVENT_MODE_CHANGE = "mode_changed"
SOCKET_CAMFI_EVENT_TIMELAPSE = "timelapse"
SOCKET_CAMFI_EVENT_TIMELAPSE_READY = "timelapse_ready"
SOCKET_CAMFI_EVENT_TIMELAPSE_ERROR = "timelapse_error"
SOCKET_CAMFI_EVENT_ERROR = "event_error"
SOCKET_CAMFI_EVENT_FILE_REMOVED = "file_removed"
SOCKET_CAMFI_EVENT_BRACKET_ERROR = "bracket_error"
SOCKET_CAMFI_EVENT_FOCUS_TRACKING_ERROR = "focusstacking_error"
SOCKET_CAMFI_EVENT_STORE_ADDED = "store_added"
SOCKET_CAMFI_EVENT_STORE_REMOVED = "store_removed"

# ----------------------------------------------------
#            REST API
# ----------------------------------------------------

REST_API_CAMFI_PROTOCOL = "http://"

"""
# IP par défaut
L'IP par défaut du viseur sans fil camfi SLR est 192.168.9.67 ou 192.168.1.67.
"""

"""
# Prenez des photos
## GET takepic/true
Déclenchez l'appareil photo pour prendre une photo.

Retourne le code d'état http 200 signifie OK, 500 signifie échoué.
Lorsque le fichier photo est généré, le serveur enverra un événement file_add au client, le paramètre d'événement est le chemin du fichier. Les clients peuvent télécharger des fichiers ou des miniatures via ce chemin.
"""

REST_API_CAMFI_GET_TAKEPIC = "/takepic/true"

"""
# Prise de vue par caméra de surveillance
## POST /tether/start
### paramètres: aucun

Accédez au mode de réception. Lorsque vous appuyez manuellement sur l'obturateur de l'appareil photo pour prendre la photo, le serveur envoie un événement file_add au client, le paramètre d'événement est le chemin du fichier. Les clients peuvent télécharger des fichiers ou des miniatures via ce chemin.
Lorsqu'une photo est supprimée de l'appareil photo, un événement file_remove est envoyé sans paramètres. Le client doit relire la liste de fichiers une fois pour actualiser la liste de fichiers.
"""

REST_API_CAMFI_POST_TETHER_START = "/tether/start"

"""
# Arrêtez la surveillance par caméra
## POST /tether/stop
Arrêtez la surveillance par caméra.
"""

REST_API_CAMFI_POST_TETHER_STOP = "/tether/stop"

"""
# Lire la liste des photos
## GET /files/$start/$count
Il listera les images sur la carte SD.

### Params ::
$start: En commençant par les premières photos, type de données entier
$count: Le nombre de photos à lire. Type de données Entier.

Si l'appel aboutit, un tableau au format suivant est renvoyé:
[Storage001 / DCIM / xxxx1.jpg, Storage001 / DCIM / xxxx2.jpg ... ]

Il est à noter que le nombre de demandes n'est pas nécessairement le même que le nombre de retours. Le nombre de feuilles retournées peut être inférieur au nombre de feuilles demandé.

Code d'état: 
    si l'exécution réussit, le code d'état http sera 200 OK
    Sinon, il renverra 500.

Python use: REST_API_CAMFI_GET_PHOTOS_LIST.format(start,count)
"""

REST_API_CAMFI_GET_PHOTOS_LIST = "/files/{}/{}"  # REST_API_CAMFI_GET_PHOTOS_LIST.format(start,count)

"""
# Télécharger l'original
## GET /raw/$filepath
Téléchargez le fichier d'origine de la caméra sur le client.

$filepathIl est basé sur le chemin de la photo renvoyé dans la commande list. Il doit être encodé en URL lors de sa transmission. Le format de codage est le suivant:
% 2Fstorage001% 2FDCIM% 2Fxxxx1.jpg.

La taille du fichier peut être obtenue dans l'auditeur renvoyé Content-Length: xxxx.
renvoie: Le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.

Python use: REST_API_CAMFI_GET_RAW_FILE.format(filepath)
"""

REST_API_CAMFI_GET_RAW_FILE = "/raw/{}"  # REST_API_CAMFI_GET_RAW_FILE.format(filepath)

"""
# Télécharger la vignette
## GET /thumbnail/$filepath
Téléchargez le fichier d'origine de la caméra sur le client.

$filepathIl est basé sur listle chemin de photo renvoyé dans la commande. Il doit être encodé en URL. Le format d'encodage est le suivant: La taille du fichier.
storage001% 2FDCIM% 2Fxxxx1.jpg.
peut être obtenue dans le fichier renvoyé. Content-Length: xxxx.
renvoie: le code d'état 200 est renvoyé avec succès, sinon le code d'état 500 est renvoyé.

Python use: REST_API_CAMFI_GET_THUMBNAIL_FILE.format(filepath)
"""

REST_API_CAMFI_GET_THUMBNAIL_FILE = "/thumbnail/{}"  # REST_API_CAMFI_GET_THUMBNAIL_FILE.format(filepath)

"""
# Télécharger l'aperçu
## GET /image/$filepath
Le téléchargement d'aperçus depuis l'appareil photo est principalement utilisé pour prévisualiser les fichiers Raw. Le format de l'aperçu de l'image est JPEG

$filepathIl est basé sur le chemin de la photo renvoyé dans la commande list. Il doit être encodé en URL lors de sa transmission. Le format de codage est le suivant:
storage001% 2FDCIM% 2Fxxxx1.jpg.
: le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.

Code d'état: si l'exécution réussit, le code d'état http sera 200 OK.
Sinon, il renverra 500.
"""

REST_API_CAMFI_GET_PREVIEW_FILE = "/image/{}"  # REST_API_CAMFI_GET_PREVIEW_FILE.format(filepath)

"""
# Vue en direct
## GET /capturemovie
Démarrez un flux vidéo en direct. L'appel de cette API créera un serveur TCP avec un port de 890. Le client peut lire le flux vidéo via le port SOCKET. Le format du flux vidéo est MJPEG.
Retour: Le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.
"""

REST_API_CAMFI_GET_START_LIVE_VIEW = "/capturemovie"

"""
## GET /stopcapturemovie
Fermez le flux vidéo et revenez: le code d'état 200 OK est retourné avec succès, sinon le code d'état 500 est retourné.
"""

REST_API_CAMFI_GET_STOP_LIVE_VIEW = "/stopcapturemovie"

"""
# Obtenir la configuration de la caméra
## GET /config
Renvoie tous les paramètres de configuration de l'appareil photo, y compris l'ouverture, l'ISO, la vitesse d'obturation et le mode d'exposition.
Exemple de résultat renvoyé:
Canon 7D
Nikon D5100
"""

REST_API_CAMFI_GET_CONFIG = "/config"

"""
# Définir la configuration de la caméra
## PUT /setconfigvalue
### Paramètres: {name:foo, value:foo}
noms Configurer et les valeurs peuvent getconfigtrouver les résultats de la commande de retour. Les appareils photo Canon et Nikon diffèrent par leurs noms et valeurs de configuration.
Renvoie: code d'état de réussite 200 OK, sinon code d'état 500.
"""

REST_API_CAMFI_PUT_CONFIG_VALUE = "/setconfigvalue"

"""
# Vérification de la version du firmware
## GET /info
Retours: {version:xxxx, serial:xxxx}
"""

REST_API_CAMFI_GET_INFO = "/info"

"""
# Obtenez une liste de WiFi à proximité
## GET /iwlist
Obtenez la liste des WiFis près de CamFi et renvoyez un tableau au format suivant:
[{
"associated": false;
"mac": "aa: 12: 12: 7a: 93: 2f";
"signal": "-72.00";
" ssid ":" xxxxxxxxx ";
}, ...]
"""

REST_API_CAMFI_GET_WIFI_LIST = "/iwlist"

"""
# Obtenir des informations sur le mode réseau
## GET /networkmode
Obtient les informations de mode réseau actuelles de CamFi et renvoie les informations au format suivant:
{
"ap_encryption": "";
"ap_ssid": "xxxxxxxxx";
"mode": "sta";
"sta_encryption": "psk2";
"sta_ssid" : "xxxxxxxxx";
}
mode: sta indique que le CamFi actuel est en mode Bridge et mode: ap indique que le CamFi actuel est en mode AP. sta_encryption représente le mode de cryptage du mot de passe de la route du pont
"""

REST_API_CAMFI_GET_NETWORK_MODE = "/networkmode"

"""
# Définir le mode réseau
## POST /networkmode
CamFi peut être réglé en mode AP ou en mode Bridge.

### Paramètres:
Mode AP: {"mode": "ap" | "sta"}
Mode Pont: {"mode": "sta", "router_ssid": foo, "mot de passe": foo, "cryptage": psk | psk2 | ...}


mode: sta indique que CamFi est réglé en mode Bridge et mode: ap indique que CamFi est réglé en mode AP.
sta_encryption représente le mode de cryptage du mot de passe-pont de routage de

retour: le succès code d'état de retour 200 OK, sinon il retourne un code d'état 500.
"""

REST_API_CAMFI_POST_NETWORK_MODE = "/networkmode"
