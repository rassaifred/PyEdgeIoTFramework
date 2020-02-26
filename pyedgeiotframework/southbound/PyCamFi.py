import os
import socket
import multiprocessing
import subprocess
import pycurl
from io import BytesIO

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyCamFi(EdgeService):

    def __int__(self):
        # ----
        super().__init__()
        # ----

    def run(self):
        # ----
        super().run()
        # ----


class CamFiTool:

    def scan_camfi(self):
        print('Mapping...')
        return map_network()

    def get_camera_info_serial(self):
        pass


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
$startEn commençant par les premières photos, type de données entier
$count: Le nombre de photos à lire. Type de données Entier.

Si l'appel aboutit, un tableau au format suivant est renvoyé:
[Storage001 / DCIM / xxxx1.jpg,
Storage001 / DCIM / xxxx2.jpg
...
]

Il est à noter que le nombre de demandes n'est pas nécessairement le même que le nombre de retours. Le nombre de feuilles retournées peut être inférieur au nombre de feuilles demandé.
Code d'état: si l'exécution réussit, le code d'état http sera 200 OK
Sinon, il renverra 500.
"""

"""
# Télécharger l'original
## GET /raw/$filepath
Téléchargez le fichier d'origine de la caméra sur le client.

$filepathIl est basé sur le chemin de la photo renvoyé dans la commande list. Il doit être encodé en URL lors de sa transmission. Le format de codage est le suivant:
% 2Fstorage001% 2FDCIM% 2Fxxxx1.jpg.

La taille du fichier peut être obtenue dans l'auditeur renvoyé Content-Length: xxxx.
renvoie: Le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.
"""

"""
# Télécharger la vignette
## GET /thumbnail/$filepath
Téléchargez le fichier d'origine de la caméra sur le client.

$filepathIl est basé sur listle chemin de photo renvoyé dans la commande. Il doit être encodé en URL. Le format d'encodage est le suivant: La taille du fichier.
storage001% 2FDCIM% 2Fxxxx1.jpg.
peut être obtenue dans le fichier renvoyé. Content-Length: xxxx.
renvoie: le code d'état 200 est renvoyé avec succès, sinon le code d'état 500 est renvoyé.
"""

"""
# Télécharger l'aperçu
## GET /image/$filepath
Le téléchargement d'aperçus depuis l'appareil photo est principalement utilisé pour prévisualiser les fichiers Raw. Le format de l'aperçu de l'image est JPEG

$filepathIl est basé sur le chemin de la photo renvoyé dans la commande list. Il doit être encodé en URL lors de sa transmission. Le format de codage est le suivant:
storage001% 2FDCIM% 2Fxxxx1.jpgReturn.
: le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.

Code d'état: si l'exécution réussit, le code d'état http sera 200 OK.
Sinon, il renverra 500.
"""

"""
# Vue en direct
## GET /capturemovie
Démarrez un flux vidéo en direct. L'appel de cette API créera un serveur TCP avec un port de 890. Le client peut lire le flux vidéo via le port SOCKET. Le format du flux vidéo est MJPEG.
Retour: Le code d'état 200 OK est renvoyé avec succès, sinon le code d'état 500 est renvoyé.

## GET /stopcapturemovie
Fermez le flux vidéo et revenez: le code d'état 200 OK est retourné avec succès, sinon le code d'état 500 est retourné.
"""

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


def pinger(job_q, results_q):

    """
    Do Ping
    :param job_q:
    :param results_q:
    :return:
    """
    DEVNULL = open(os.devnull, 'w')
    while True:

        ip = job_q.get()

        if ip is None:
            break

        try:
            subprocess.check_call(['ping', '-c1', ip],
                                  stdout=DEVNULL)
            results_q.put(ip)
        except:
            pass


def get_my_ip():
    """
    Find my IP address
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def map_network(pool_size=255):
    """
    Maps the network
    :param pool_size: amount of parallel ping processes
    :return: list of valid ip addresses
    """

    ip_list = list()

    # get my IP and compose a base like 192.168.1.xxx
    ip_parts = get_my_ip().split('.')
    # base_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    base_ip = ip_parts[0] + '.' + ip_parts[1] + '.9.'

    # prepare the jobs queue
    jobs = multiprocessing.Queue()
    results = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=pinger, args=(jobs, results)) for i in range(pool_size)]

    for p in pool:
        p.start()

    # cue hte ping processes
    for i in range(1, 255):
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
        socket.setdefaulttimeout(1)

        # returns 0 if connection succeeds else raises error
        result = socket_obj.connect_ex((ip, 8080))  # address and port in the tuple format

        # print(ip, "-", result)

        # closes te object
        socket_obj.close()

        if result == 0:

            url_str = "{}{}{}".format(REST_API_CAMFI_PROTOCOL, ip, REST_API_CAMFI_GET_INFO)

            print(url_str)
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
            print('Output of GET request:\n%s' % get_body.decode('utf8'))

            if get_body:
                #
                ip_list.append(ip)

    return ip_list

