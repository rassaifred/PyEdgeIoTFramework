"""
ToDo: make static ip e.g: 192.168.1.255 next time use local.orbitip.server with security param in Global Env Var
ToDo: make endpoint to control Orbite IP devices
ToDo: make bridge Orbite IP <=> PyPubSub
"""
import datetime
import binascii
import falcon

from sqlitedict import SqliteDict

from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyOrbiteip(EdgeService):
    # ----
    NEW_TAG_TOPIC = "NEW_TAG"
    LOST_TAG_TOPIC = "LOST_TAG"
    INIT_READER = "INIT_READER"
    NO_TAG_STRING = "NO_TAG"
    # ----
    init_state_contact = True
    # ----
    sessions = {}
    # ----
    app = None
    # ----

    def __int__(self):
        # ----
        EdgeService.__init__(self)
        # ----

    def run(self) -> None:
        # ----
        EdgeService.run(self)
        # ----
        # Resources are represented by long-lived class instances
        # things will handle all requests to the '/things' URL path
        if self.app:
            self.app.add_route('/orbitip.php', self)

    def stringifier(self, tmp):
        if tmp is not self.NO_TAG_STRING:
            try:
                tmp_str = binascii.hexlify(tmp)
                return '0x{0}'.format(tmp_str.decode("utf-8"))
            except:
                return tmp
        else:
            return tmp

    def add_session(self, uid=None, device_id=None):
        if uid and device_id:
            # add session uid
            # ---
            mydict = SqliteDict('./db.sqlite', autocommit=True)
            mydict[str(device_id)] = self.stringifier(uid)
            for key, value in mydict.iteritems():
                self.sessions[key] = value
            mydict.close()
            # --
            print(self.sessions)


    def sessions_check(self):
        # ---
        pass
        # ---
        """
        for item in sessions:
            itt = int(sessions[str(item)])
            new_itt = itt
            # ---
            old_tag_presence_state: bool = False
            new_tag_presence_state: bool = False
            # ---
            if itt > 0:
                old_tag_presence_state = True
                new_itt -= 1
            # ---
            if new_itt > 0:
                new_tag_presence_state = True
            # ---
            sessions.update({str(item): new_itt})
            # ---
            if old_tag_presence_state != new_tag_presence_state:
                if new_tag_presence_state:
                    print("1 -- > new tag")
                else:
                    print("0 -- > lost tag")
            # ---
        # ---
        # print("---->", sessions)
        """

    def on_get(self, req, resp):
        """Handles GET requests"""
        # ---
        # ---
        curr_time = datetime.datetime.now()  # ('Y-m-d H:i:s', time());
        st = curr_time.strftime("%Y-%m-%d %H:%M:%S")
        # ui =
        # ---
        cmd = req.get_param("cmd")
        mac = req.get_param("mac")
        relay = req.get_param("relay")
        sd = req.get_param("sd")
        device_id = req.get_param("id")
        # ---
        # print("--> ", cmd)
        # ---
        """Handles GET requests"""
        # ---
        resp.status = falcon.HTTP_200  # This is the default status
        # ---
        response_str = ''
        # ---
        """
        $cmd=PU is sent once after the reader is powered up.
        $cmd=CO is sent when a card is detected by the reader.
        $cmd=HB is sent at regular intervals – this is a programmed heartbeat rate. The default value is 30 seconds.
        $cmd=SW is sent when a level change is detected either on digital Input 1 or Input 2.
        $cmd=PG is sent when the reader received a “ping” request.
        $cmd=CB is sent when an offline stored message is transmitted
        """

        """
        HB --> 60
        SN Interval --> 300
        v4.0.5
        """

        """
        # response_str += 'MKEY=BA637F128CCDC\r\n'
        # response_str += 'MREAD=B04\r\n'
        # response_str += 'MAUTH=1\r\n'
        # response_str += 'MD5=53306C757421306E\n'
        # response_str += 'SID=ABBA0123\n'
        # response_str += 'WS=192.168.1.54\n'
        # response_str += 'EXT=0\t'
        # response_str += 'HB=10\t'
        # response_str += 'RLY=1\t'
        # response_str += 'BEEP = 1\t'
        # response_str += 'RCR = 37\t'
        # response_str += 'PBKT = 1000'
        """
        if cmd == 'PU':
            response_str += 'CK={}\n'.format(st)
            pass
        elif cmd == 'CO':
            uid =req.get_param("uid")
            # ---
            self.add_session(uid=uid, device_id=device_id)
            # ---
            # print(sessions)
            # ---
            # print("uid --> ", uid)
            response_str += 'BEEP=0\t'
            response_str += 'RCR=3\t'
            response_str += 'PBKT=200\t'
        elif cmd == 'HB':
            # verif
            # response_str += 'CK={}'.format(st)
            pass
        elif cmd == 'SW':
            # is sent when a level change is detected either on digital Input 1
            sw_state = bool(int(req.get_param("contact1")))
            if sw_state is not self.init_state_contact:
                self.add_session(uid=self.NO_TAG_STRING, device_id=device_id)

        elif cmd == 'PG':
            pass
        elif cmd == 'CB':
            pass
        else:
            response_str += 'CK={}'.format(st)

        # print("response --> ", response_str)
        # ---
        resp.body = ('<html><body><ORBIT>%s</ORBIT></body></html>' % response_str)
