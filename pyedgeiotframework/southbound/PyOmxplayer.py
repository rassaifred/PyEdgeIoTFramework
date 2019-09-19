"""
ToDo: (issue critic) omxplayer dbus lose connection
ToDo: add default media
ToDo: add idle mode
ToDo: add download mode

"""

import json
from omxplayer.player import OMXPlayer
from PyEdgeIoTFramework.pyedgeiotframework.core.EdgeService import EdgeService


class PyOmxplayer(EdgeService):

    # MQTT LOCAL TOPIC
    CURRENT_VIDEO_CHANGE_TOPIC = "current_video_change_topic"
    LOCAL_PLAYLIST_READY_TOPIC = "local_playlist_ready_topic"
    MUTE_TOPIC = "mute_topic"
    RENDRER_IS_READY_TOPIC = "rendrer_is_ready_topic"

    # PubSub TOPIC
    LOCAL_MQTT_CONNECTED_TOPIC = "local_mqtt_connected_topic"

    current_playlist = []
    curr_index = -1

    player = None
    mutting = True
    voltmp = '0'

    def __int__(self):
        # ----
        EdgeService.__init__(self)
        # ----

    def run(self) -> None:
        # ----
        EdgeService.run(self)
        # ----
        self.subscribe_command(callback=self.update_playlist, topic=self.LOCAL_PLAYLIST_READY_TOPIC)
        self.subscribe_command(callback=self.mute_player, topic=self.MUTE_TOPIC)
        self.subscribe_command(callback=self.player_ready_callback, topic=self.LOCAL_MQTT_CONNECTED_TOPIC)
        # ----

    def play_asset(self):
        if len(self.current_playlist)>0:
            asset_id = self.current_playlist[self.curr_index]["scheduleVideoId"]
            uri = self.current_playlist[self.curr_index]["uri"]
            # ----
            print("play asset with id:{0} and uri:{1}".format(str(asset_id), str(uri)))
            # ----
            if self.player:
                self.quitPlayer()
            # ----
            # print("etape 1")
            # ----
            self.voltmp = '0'
            # ----
            if self.mutting:
                self.voltmp = '-6000'
            # ----
            # print("etape 2")
            # ----
            self.player = OMXPlayer(str(uri), args=['-b', '--no-osd', '--no-keys', '--blank=0xFF000000', '--vol', self.voltmp])
            # ----
            # print("etape 3")
            # print(self.player.)
            # ----
            self.player.playEvent += lambda _: print("event Play")
            self.player.pauseEvent += lambda _: print("event Pause")
            self.player.stopEvent += lambda _: print("event Stop")
            self.player.exitEvent += lambda _, __: self.exit_callback()
            # ----
            self.dispatch_event(
                topic=self.CURRENT_VIDEO_CHANGE_TOPIC,
                payload=str(self.current_playlist[self.curr_index])
            )
            # ----
        else:
            print("no asset to play")
        # ----

    def play_next_asset(self):
        #print("play next asset")
        # ----
        self.curr_index += 1
        # ----
        if self.curr_index > len(self.current_playlist) - 1:
            self.curr_index = 0
        # ----
        self.play_asset()

    def play_previous_asset(self):
        self.curr_index -= 1
        # ----
        if self.curr_index < 0:
            self.curr_index = len(self.current_playlist) - 1
        # ----
        self.play_asset()

    def idle_rendrer(self):
        # ---- display loading
        pass

    def player_ready_callback(self, payload=None):
        if len(self.current_playlist) == 0:
            # ----
            self.dispatch_event(
                topic=self.RENDRER_IS_READY_TOPIC
            )

    def mute_player(self, payload=None):
        # -----
        # print("mute player callback")
        # -----
        # self.mutting = bool(int(payload))
        # -----
        if bool(int(payload)):
            self.mute()
        else:
            self.unmute()

    def update_playlist(self, payload=None):
        # ----
        #print("update playlist", payload)
        # ----
        data = None
        try:
            data = json.loads(payload.decode("utf-8"))
        except:
            try:
                data = json.loads(payload)
            except:
                print("data error")
        # ----
        # print("data:", data)
        # ----
        tmp_list = data["assets"]
        # ----
        # print("tmp_list: ", tmp_list)
        # ----
        if len(tmp_list) > 0:
            self.curr_index = -1
            self.current_playlist = tmp_list
            self.play_next_asset()

    def mute(self):
        if self.mutting:
            # print("deja mute")
            pass
        else:
            print("mute")
            self.mutting = True
            self.player.set_volume(0)

    def unmute(self):
        if self.mutting:
            #print("unmute")
            self.mutting = False
            self.player.set_volume(1)
        else:
            #print("deja unmute")
            pass

    def exit_callback(self):
        #print("event Exit ")
        self.play_next_asset()

    def quitPlayer(self):
        #print("quit player")
        self.player.quit()