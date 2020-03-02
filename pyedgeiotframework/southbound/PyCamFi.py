"""
ToDo: verify if camfi-adress
ToDo: ok - get camfi infos
ToDO: ok - get camera config
ToDo: ok - add socket client camfi on PyCamFi
ToDO: ok - add socket event handler on PyCamFi
ToDo: ok - add events listener -> subscribe to camfi events topics
"""

import requests
import json
from socketIO_client import SocketIO, LoggingNamespace

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLR import PyDSLR


class PyCamFi(EdgeService):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.camera = PyDSLR()
        # ----
        self.ip_adress = "0.0.0.0"
        self.version = "0"
        self.serial = "0"
        self.used = .0
        self.SSID = "-"
        self.mac = "-"
        self.network_mode = "-"
        # ----
        self.socketIO = None
        # ----

    def run(self):
        # ----
        super().run()
        # ----
        print("camfi added with ip adress: {} infos: {}".format(self.ip_adress, self.get_camfi_info()))
        # ----
        # get camera config
        # ----
        data = self.get_camera_config()
        # ----
        if data:
            try:
                # x.main.children.status.children.cameramodel.value
                self.camera.cameramodel = data["main"]["children"]["status"]["children"]["cameramodel"]["value"]
                self.camera.deviceversion = data["main"]["children"]["status"]["children"]["deviceversion"]["value"]
                self.camera.eosserialnumber = data["main"]["children"]["status"]["children"]["eosserialnumber"]["value"]
                self.camera.serialnumber = data["main"]["children"]["status"]["children"]["serialnumber"]["value"]
            except:
                pass
        # ----
        # add socket Client
        # ----
        self.socketIO = SocketIO(self.ip_adress, PyCamFi.SOCKET_CAMFI_PORT, LoggingNamespace)
        self.socketIO.on('connect', self.on_connect)
        # ---
        self.socketIO.on(PyCamFi.SOCKET_CAMFI_EVENT_CAMERA_REMOVE, self.on_camera_remove)
        self.socketIO.on(PyCamFi.SOCKET_CAMFI_EVENT_CAMERA_ADD, self.on_camera_add)
        self.socketIO.on(PyCamFi.SOCKET_CAMFI_EVENT_FILE_ADDED, self.on_file_added)
        self.socketIO.on(PyCamFi.SOCKET_CAMFI_EVENT_LIVESHOW_ERROR, self.on_liveshow_error)
        self.socketIO.on(PyCamFi.SOCKET_CAMFI_EVENT_TIMELAPSE_ERROR, self.on_timelaspe_error)
        # ---
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        # ----
        self.socketIO.wait()
        # ----
        # start tethring
        # ----
        self.start_tethring()

    # ----------------------------------------------------
    #                   REST API
    # ----------------------------------------------------

    def get_camfi_info(self):
        get_url = "{}{}{}".format(PyCamFi.REST_API_CAMFI_PROTOCOL, self.ip_adress, PyCamFi.REST_API_CAMFI_GET_INFO)
        r = requests.get(get_url)
        return r.json()

    def get_camera_config(self):
        get_url = "{}{}{}".format(PyCamFi.REST_API_CAMFI_PROTOCOL, self.ip_adress, PyCamFi.REST_API_CAMFI_GET_CONFIG)
        r = requests.get(get_url)
        return r.json()

    def start_tethring(self):
        post_url = "{}{}{}".format(PyCamFi.REST_API_CAMFI_PROTOCOL, self.ip_adress, PyCamFi.REST_API_CAMFI_GET_TAKEPIC)
        r = requests.post(post_url)
        return r.json()

    def stop_tethring(self):
        post_url = "{}{}{}".format(PyCamFi.REST_API_CAMFI_PROTOCOL, self.ip_adress, PyCamFi.REST_API_CAMFI_POST_TETHER_STOP)
        r = requests.post(post_url)
        return r.json()

    # ----------------------------------------------------
    #                   SOCKET API
    # ----------------------------------------------------

    def on_connect(self):
        print('connect')

    def on_disconnect(self):
        print('disconnect')

    def on_reconnect(self):
        print('reconnect')

    def on_camera_remove(self):
        self.start_tethring()
        # ---
        data = json.dumps({"camera_id": self.camera.eosserialnumber, "gateway": self.ip_adress})
        print('camera_remove', data)
        # ---
        self.dispatch_event(topic=str(PyCamFi.CAMFI_CAMERA_REMOVED_TOPIC), payload=data)
        # ---

    def on_camera_add(self, *args):
        self.start_tethring()
        # ---
        data = json.dumps(args)
        tmp_dct = json.loads(data)
        tmp_dct[0]["camera_id"] = self.camera.eosserialnumber
        tmp_dct[0]["gateway"] = self.ip_adress
        data = json.dumps(tmp_dct[0])
        print('camera_add', data)
        # ---
        self.dispatch_event(topic=str(PyCamFi.CAMFI_CAMERA_ADDED_TOPIC), payload=data)
        # ---

    def on_file_added(self, *args):
        self.start_tethring()
        # ---
        data = json.dumps(args)
        tmp_dct = json.loads(data)
        transform_dict = {"camera_id": self.camera.eosserialnumber, "gateway": self.ip_adress, "file_added": tmp_dct[0]}
        data = json.dumps(transform_dict)
        print('file_added', data)
        # ---
        self.dispatch_event(topic=str(PyCamFi.CAMFI_FILE_ADDED_TOPIC), payload=data)
        # ---

    def on_liveshow_error(self, *args):
        print('liveshow_error', args)

    def on_timelaspe_error(self, *args):
        print('timelaspe_error', args)

    # ----------------------------------------------------
    #            TOPIC's
    # ----------------------------------------------------

    CAMFI_CAMERA_ADDED_TOPIC = "CAMFI_CAMERA_ADDED"
    CAMFI_CAMERA_REMOVED_TOPIC = "CAMFI_CAMERA_REMOVED"
    CAMFI_FILE_ADDED_TOPIC = "CAMFI_FILE_ADDED"

    # ----------------------------------------------------
    #            SOCKET CONFIG
    # ----------------------------------------------------

    SOCKET_CAMFI_PORT = 8080

    # ----------------------------------------------------
    #            SOCKET EVENTS
    # ----------------------------------------------------

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
