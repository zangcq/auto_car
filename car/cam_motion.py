import requests
import os

class CamMotion:
    def __init__(self, ip, control_port):
        self.ip = ip
        self.control_port = control_port

    def check(self):
        # 这是在小车，所以直接localhost就行
        requests.get("http://%s:%s/0/action/snapshot" % ('127.0.0.1', self.control_port))

    def get_last_snap(self):
        data = None
        file_size = os.path.getsize('/home/pi/motion/lastsnap.jpg')
        with open('/home/pi/motion/lastsnap.jpg', 'rb')as fin:
            data = fin.read()
        return data, file_size
