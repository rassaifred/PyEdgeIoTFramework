"""

ToDo: make static ip e.g: 192.168.1.255 next time use local.orbitip.server with security param in Global Env Var
ToDo: make endpoint to control Orbite IP devices
ToDo: make bridge Orbite IP <=> PyPubSub

Example of a request sent to the server upon ‘ping’
"GET /orbit.php?cmd=PG&sid=&dhcp=1&dns=0&ws=192.168.7.191&pt=80&gw=192.168.7.1& nm=255.255.255.0&mac=54:10:EC:9C:73:67&psrc=192.168.7.191&relay=1&sd=0&dat e=2018/12/05&time=16:54:28&md5=5CE8BFA042CC831F69CFDEC61ABFE12D&contact1=1 &contact2=1&ver=2.2.0&id=192.168.7.60&rn=D9F1A0B0C1A88E4E& HTTP/1.0" 200 397 "-" "ORBIT-HTTP-CLIENT"
Example of a request sent to the server upon card detection
"GET /orbit.php?cmd=CO&id=192.168.7.219&sid=&uid=0E980F53&ulen=4&date=2018/12/0 6&time=09:12:36&md5=35EBCB79E169D889E638AEFE8EB715C6&mac=54:10:EC:9C:42:12 & HTTP/1.0" 200 354 "-" "ORBIT-HTTP-CLIENT"
Example of a request sent to the server upon reader power up
"GET /orbit.php?cmd=PU&id=192.168.7.244&mac=54:10:EC:9C:5F:B9&ver=2.2.0&blver=0 0000201&sd=0& HTTP/1.0" 200 433 "-" "ORBIT-HTTP-CLIENT"
Example of a regular heartbeat request sent to the server
"GET /orbit.php?cmd=HB&id=192.168.7.227&RE=0&mac=54:10:EC:9C:73:9E& HTTP/1.0" 200 337 "-" "ORBIT-HTTP-CLIENT"
Example of a regular sw request sent to the server
"GET /orbitip.php?cmd=SW&sid=&date=2020/01/03&time=19:22:01&md5=286A483AD990E95A2C6815B5AC9E98A5&contact1=0&contact2=1&id=192.168.1.208& HTTP/1.0" 200 337 "-" "ORBIT-HTTP-CLIENT"

$cmd=PU is sent once after the reader is powered up.
$cmd=CO is sent when a card is detected by the reader.
$cmd=HB is sent at regular intervals – this is a programmed heartbeat rate. The default value is 30 seconds.
$cmd=SW is sent when a level change is detected either on digital Input 1 or Input 2.
$cmd=PG is sent when the reader received a “ping” request.
$cmd=CB is sent when an offline stored message is transmitted

HB --> 60
SN Interval --> 300
v4.0.5

response_str += 'MKEY=BA637F128CCDC\r\n'
response_str += 'MREAD=B04\r\n'
response_str += 'MAUTH=1\r\n'
response_str += 'MD5=53306C757421306E\n'
response_str += 'SID=ABBA0123\n'
response_str += 'WS=192.168.1.54\n'
response_str += 'EXT=0\t'
response_str += 'HB=10\t'
response_str += 'RLY=1\t'
response_str += 'BEEP = 1\t'
response_str += 'RCR = 37\t'
response_str += 'PBKT = 1000'
response_str += 'RBT= = 1000'

"""

import datetime
import falcon
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyOrbiteip(EdgeService):
    # ----
    NEW_TAG_TOPIC = "NEW_TAG"
    READ_CARD_TAG_TOPIC = "READ_CARD_TAG"
    LOST_TAG_TOPIC = "LOST_TAG"
    INIT_READER = "INIT_READER"
    NO_TAG_STRING = "NO_TAG"
    SWITCH_CHANGE_TOPIC = "SWITCH_CHANGE"
    # ----
    app = None
    # ----
    first_run = True
    # ----
    init_state_contact1 = True
    # ----

    def __int__(self):
        # ----
        super().__init__()
        # ----

    def run(self):
        # ----
        super().run()
        # ----
        # Resources are represented by long-lived class instances
        # things will handle all requests to the '/things' URL path
        if self.app:
            self.app.add_route('/orbitip.php', self)

    def on_get(self, req, resp):
        # ---
        # print("\n*-::-*-:GET start:-*-::-*", datetime.datetime.utcnow())
        # ---
        curr_time = datetime.datetime.now()  # ('Y-m-d H:i:s', time());
        # ---
        st = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        # ---
        cmd = req.get_param("cmd")
        mac = req.get_param("mac")
        relay = req.get_param("relay")
        sd = req.get_param("sd")
        md5 = req.get_param("md5")
        device_id = req.get_param("id")
        # ---
        response_str = ''
        # ---
        if cmd == 'PU':
            response_str += 'CK={}\n'.format(st)
            response_str += 'HB=10\t'
        elif cmd == 'CO':
            # ---
            uid = req.get_param("uid")
            # ---
            # print("uid --> ", uid)
            # response_str += 'BEEP=1\t'
            response_str += 'RCR=3\t'
            response_str += 'PBKT=10\t'
            # ---
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # print("orbit read start ---> ", datetime.datetime.utcnow())
            # ---
            self.dispatch_event(
                topic=self.READ_CARD_TAG_TOPIC,
                payload={
                    "port": device_id,
                    "uid": uid
                }
            )
            # ---
            # print("orbit read end ---> ", datetime.datetime.utcnow())
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # ---
        elif cmd == 'HB':
            # verif
            # response_str += 'CK={}'.format(st)
            pass
        elif cmd == 'SW':
            # is sent when a level change is detected either on digital Input 1
            sw_state = req.get_param("contact1")
            # ---
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # print("orbit sw start ---> ", datetime.datetime.utcnow())
            # ---
            if bool(int(sw_state)) is self.init_state_contact1:
                # ---
                self.dispatch_event(
                    topic=self.SWITCH_CHANGE_TOPIC,
                    payload={
                        "port": device_id,
                        "state": sw_state
                    }
                )
                # ---
            # ---
            # print("orbit sw end ---> ", datetime.datetime.utcnow())
            # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            # ---
        elif cmd == 'PG':
            # ---
            if self.first_run:
                response_str += 'RBT={}\t'.format(md5)
                self.first_run = False
        elif cmd == 'CB':
            pass
        # ---
        response_body = '<html><body><ORBIT>%s</ORBIT></body></html>' % response_str
        # ---
        # print("cmd:", cmd, req, "resp:", response_body)
        # ---
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = response_body
        # ---
        # print("*-::-*-:GET end :-*-::-*{}\n".format(datetime.datetime.utcnow()))
