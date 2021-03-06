"""

ToDo: ok - get camfi infos
ToDO: ok - get camera config
ToDo: ok - add socket client camfi on PyDSLRCamFiGateway
ToDO: ok - add socket event handler on PyDSLRCamFiGateway
ToDo: ok - add events listener -> subscribe to camfi events topics
ToDo: ok - add eosserialnuber to copyright automatic form API
ToDo: ok - add camera_order from CamFi config infos
ToDo: add losing camfi scenario

"""

import requests
import urllib.parse
import json
from socketIO_client import SocketIO, LoggingNamespace

from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLRGateway import PyDSLRGateway
from PyEdgeIoTFramework.pyedgeiotframework.southbound.PyDSLR import PyDSLR


class PyDSLRCamFiGateway(PyDSLRGateway):

    def __init__(self):
        # ----
        super().__init__()
        # ----
        self.version = "0"
        self.serial = "0"
        self.used = .0
        self.SSID = "-"
        self.network_mode = "-"
        # ----
        self.socketIO = None
        # ----

    def run(self):
        # ----
        super().run()
        # ----
        # get camera config
        # ----
        data = self.get_camera_config()
        # ----
        if "main" in data.keys():
            # ---
            if data["main"]["children"]["status"]["children"]["cameramodel"]["value"]:
                # x.main.children.status.children.cameramodel.value
                self.camera.cameramodel = data["main"]["children"]["status"]["children"]["cameramodel"]["value"]
            # ---
            if data["main"]["children"]["status"]["children"]["deviceversion"]["value"]:
                self.camera.deviceversion = data["main"]["children"]["status"]["children"]["deviceversion"]["value"]
            # ---
            if data["main"]["children"]["status"]["children"]["eosserialnumber"]["value"]:
                # ---
                self.camera.eosserialnumber = data["main"]["children"]["status"]["children"]["eosserialnumber"]["value"]
                # ---
                tmp_config_name = data["main"]["children"]["settings"]["children"]["artist"]["value"]
                # ---
                result_set_order = self.camera.set_camera_order_from_config_name(
                    #   x.main.children.settings.children.artist.value
                        tmp_config_name
                )
                # ---
                # print("tmp_config_name:", tmp_config_name, result_set_order)
                # ---
                if not result_set_order:
                    self.put_camera_config(
                        config_name=self.REST_API_CAMFI_ARTIST_CONFIG_NAME,
                        config_value="order={}".format(self.camera.camera_order)
                    )
                # ---
            # ---
            if data["main"]["children"]["status"]["children"]["serialnumber"]["value"]:
                self.camera.serialnumber = data["main"]["children"]["status"]["children"]["serialnumber"]["value"]
            # ---

            # ---
            # copyright
            # ---

            # ----
            # set copyright value as eosserialnumber in camera via camfi
            # ----
            self.put_camera_config(
                config_name=self.REST_API_CAMFI_COPYRIGHT_CONFIG_NAME,
                config_value=self.camera.eosserialnumber
            )
        # ----
        # get camfi info
        # ----
        info_data = self.get_camfi_info()
        # ----
        if info_data:
            # ----
            if info_data["version"]:
                self.version = info_data["version"]
            # ----
            if info_data["serial"]:
                self.serial = info_data["serial"]
            # ----
            if info_data["used"]:
                self.used = float(info_data["used"])
            # ----
            data = json.dumps(
                dict(
                    camera_id=self.camera.eosserialnumber,
                    gateway_ip=self.gateway_ip,
                    camera_order=self.camera.camera_order
                )
            )
            # ----
            # print('camera_add', data)
            # ----
            self.dispatch_event(
                topic=str(PyDSLR.CAMERA_ADDED_TOPIC),
                payload=data
            )
            # ----
        # ----
        # add socket Client
        # ----
        self.socketIO = SocketIO(
            self.gateway_ip,
            PyDSLRCamFiGateway.SOCKET_CAMFI_PORT,
            LoggingNamespace
        )
        # ----
        self.socketIO.on(
            'connect',
            self.on_camfi_socket_connect
        )
        # ---
        self.socketIO.on(
            PyDSLRCamFiGateway.SOCKET_CAMFI_EVENT_CAMERA_REMOVE,
            self.on_camfi_socket_camera_remove
        )
        # ---
        self.socketIO.on(
            PyDSLRCamFiGateway.SOCKET_CAMFI_EVENT_CAMERA_ADD,
            self.on_camfi_socket_camera_add
        )
        # ---
        self.socketIO.on(
            PyDSLRCamFiGateway.SOCKET_CAMFI_EVENT_FILE_ADDED,
            self.on_camfi_socket_file_added
        )
        # ---
        self.socketIO.on(
            PyDSLRCamFiGateway.SOCKET_CAMFI_EVENT_LIVESHOW_ERROR,
            self.on_camfi_socket_liveshow_error
        )
        # ---
        self.socketIO.on(
            PyDSLRCamFiGateway.SOCKET_CAMFI_EVENT_TIMELAPSE_ERROR,
            self.on_camfi_socket_timelaspe_error
        )
        # ---
        self.socketIO.on(
            'disconnect',
            self.on_camfi_socket_disconnect
        )
        self.socketIO.on(
            'reconnect',
            self.on_camfi_socket_reconnect
        )
        # ----
        self.socketIO.wait()
        # ----
        # start tethring
        # ----
        self.start_tethring()
        # ----

    # ----------------------------------------------------
    #                   Methodes
    # ----------------------------------------------------

    def set_camera_order(self, tmp_order=None):
        # ---
        super(self).set_camera_order(tmp_order)
        # ---
        if tmp_order:
            # ---
            # set camera order info over camfi
            # ---
            self.put_camera_config(
                config_name=self.REST_API_CAMFI_ARTIST_CONFIG_NAME,
                config_value=str(tmp_order)
            )
            # ---

    def get_photo_from_camera(self, payload=None):
        # ----
        super().get_photo_from_camera(payload=payload)
        # ----
        tmp_dct = json.loads(payload)
        # ----
        tmp_file_added_path = tmp_dct["file_added"]
        # ---
        photo_data = self.get_raw_file(
            tmp_ip=self.gateway_ip,
            path=tmp_file_added_path
        )
        # ---
        return photo_data
        # ----

    # ----------------------------------------------------
    #                   REST API
    # ----------------------------------------------------

    def get_camfi_info(self, tmp_ip=None):

        if not tmp_ip:
            tmp_ip = self.gateway_ip

        get_url = "{}{}{}".format(
            PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
            tmp_ip,
            PyDSLRCamFiGateway.REST_API_CAMFI_GET_INFO
        )

        try:
            r = requests.get(get_url)
            return r.json()
        except:
            pass

    def get_camera_config(self, tmp_ip=None):
        if not tmp_ip:
            tmp_ip = self.gateway_ip

        get_url = "{}{}{}".format(
            PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
            tmp_ip,
            PyDSLRCamFiGateway.REST_API_CAMFI_GET_CONFIG
        )

        r = requests.get(get_url)
        return r.json()

    def put_camera_config(self, tmp_ip=None, config_name=None, config_value=None):
        if not tmp_ip:
            tmp_ip = self.gateway_ip

        put_url = "{}{}{}".format(
            PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
            tmp_ip,
            PyDSLRCamFiGateway.REST_API_CAMFI_PUT_CONFIG_VALUE
        )

        headers = {'Content-Type': 'application/json'}

        tmp_dict = dict(
            name=config_name,
            value=config_value
        )

        tmp_data = json.dumps(tmp_dict)

        if config_name:
            r = requests.put(put_url, data=tmp_data, headers=headers)
            # return r.json()
            # print("put_camera_config", put_url, tmp_data, headers, r)
            # ----
            self.start_tethring()
            # ----

    def start_tethring(self, tmp_ip=None):
        if not tmp_ip:
            tmp_ip = self.gateway_ip

        post_url = "{}{}{}".format(
            PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
            tmp_ip,
            PyDSLRCamFiGateway.REST_API_CAMFI_POST_TETHER_START
        )

        r = requests.post(post_url)
        # return r.json()

    def stop_tethring(self, tmp_ip=None):
        if not tmp_ip:
            tmp_ip = self.gateway_ip

        post_url = "{}{}{}".format(
            PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
            tmp_ip,
            PyDSLRCamFiGateway.REST_API_CAMFI_POST_TETHER_STOP
        )

        r = requests.post(post_url)
        # return r.json()

    def get_raw_file(self, tmp_ip=None, path=None):
        if not tmp_ip:
            tmp_ip = self.gateway_ip

        if path:
            tmp_path = urllib.parse.quote(path,safe='')

            get_url = "{}{}{}{}".format(
                PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
                tmp_ip,
                PyDSLRCamFiGateway.REST_API_CAMFI_GET_RAW_FILE,
                tmp_path
            )

            r = requests.get(get_url)
            return r

    def get_preview_file(self, tmp_ip=None, path=None):
        if not tmp_ip:
            tmp_ip = self.gateway_ip

        if path:
            tmp_path = urllib.parse.quote(path, safe='')

            get_url = "{}{}{}{}".format(
                PyDSLRCamFiGateway.REST_API_CAMFI_PROTOCOL,
                tmp_ip,
                PyDSLRCamFiGateway.REST_API_CAMFI_GET_PREVIEW_FILE,
                tmp_path
            )

            r = requests.get(get_url)
            return r

    # ----------------------------------------------------
    #                   SOCKET API
    # ----------------------------------------------------

    def on_camfi_socket_connect(self):
        # ----
        self.dispatch_event(
            topic=self.DSLR_GATEWAY_READY_TOPIC,
            payload=json.dumps(
                dict(
                    gateway_ip=self.gateway_ip,
                    camera_id=self.camera.camera_id
                )
            )
        )
        # ----

    def on_camfi_socket_disconnect(self):
        print('camfi_socket_disconnect')

    def on_camfi_socket_reconnect(self):
        print('camfi_socket_reconnect')

    def on_camfi_socket_camera_remove(self):
        # ---
        self.start_tethring()
        # ---
        data = json.dumps(
            dict(
                camera_id=self.camera.eosserialnumber,
                gateway_ip=self.gateway_ip,
                camera_order=self.camera.camera_order
            )
        )
        # ---
        self.dispatch_event(
            topic=str(PyDSLR.CAMERA_REMOVED_TOPIC),
            payload=data
        )
        # ---

    def on_camfi_socket_camera_add(self, *args):
        # ToDo: a ameliorer
        # ---
        self.start_tethring()
        # ---
        data = json.dumps(args)
        # ---
        tmp_dct = json.loads(data)
        # ---
        tmp_dct[0]["camera_id"] = self.camera.eosserialnumber
        tmp_dct[0]["gateway_ip"] = self.gateway_ip
        tmp_dct[0]["camera_order"] = self.camera.camera_order
        # ---
        data = json.dumps(tmp_dct[0])
        # ---
        self.dispatch_event(
            topic=str(PyDSLR.CAMERA_ADDED_TOPIC),
            payload=data
        )
        # ---

    def on_camfi_socket_file_added(self, *args):
        # ---
        self.start_tethring()
        # ---
        data = json.dumps(args)
        # ---
        tmp_dct = json.loads(data)
        # ---
        tmp_file_added_path = tmp_dct[0]
        # ---
        transform_dict = dict(
            camera_id=self.camera.eosserialnumber,
            gateway_ip=self.gateway_ip,
            camera_order=self.camera.camera_order,
            file_added=tmp_file_added_path
        )
        # ---
        data = json.dumps(transform_dict)
        # ---
        self.on_file_added(payload=data)
        # ---

    def on_camfi_socket_liveshow_error(self, *args):
        print('camfi_socket_liveshow_error', args)

    def on_camfi_socket_timelaspe_error(self, *args):
        print('camfi_socket_timelaspe_error', args)

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
    #            CONFIG NAME
    # ----------------------------------------------------

    REST_API_CAMFI_COPYRIGHT_CONFIG_NAME = "copyright"
    REST_API_CAMFI_ARTIST_CONFIG_NAME = "artist"

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
    
    $filepath Il est basé sur le chemin de la photo renvoyé dans la commande list. Il doit être encodé en URL lors de sa transmission. 
    Le format de codage est le suivant:
    % 2Fstorage001% 2FDCIM% 2Fxxxx1.jpg.
    
    La taille du fichier peut être obtenue dans l'auditeur renvoyé Content-Length: xxxx.
    renvoie: Le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.
    
    Python use: REST_API_CAMFI_GET_RAW_FILE.format(filepath)
    """

    REST_API_CAMFI_GET_RAW_FILE = "/raw/"  # REST_API_CAMFI_GET_RAW_FILE.format(filepath)

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

    REST_API_CAMFI_GET_PREVIEW_FILE = "/image/"  # REST_API_CAMFI_GET_PREVIEW_FILE.format(filepath)

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
    Configurer et les valeurs peuvent get config trouver les résultats de la commande de retour. 
    Les appareils photo Canon et Nikon diffèrent par leurs noms et valeurs de configuration.
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
