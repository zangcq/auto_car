#coding:utf8
"""socketserver在小车端，因为要控制小车的运动，是pc向小车发送指令"""
import os
from socketserver import BaseRequestHandler, TCPServer
from Car import Car
import configparser
from cam_motion import CamMotion

block_size = 1024

def read_config():
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    return cf


class ResponseHandler(BaseRequestHandler):
    global my_car

    def handle(self):
        # self.request.settimeout(3)
        while True:
            try:
                # 接收控制指令。与客户端约定好mapping
                operation = self.request.recv(block_size).strip()
                # TODO: 嵌入拍照的处理
                if operation:
                    print(operation)
                    if str(operation.decode('utf8')) == 'start':
                        cam.check()
                        send_size = 0
                        file_size = os.path.getsize('/home/pi/motion/lastsnap.jpg')
                        print(file_size)
                        self.request.sendall(bytes(str(file_size), 'utf8'))
                        with open('/home/pi/motion/lastsnap.jpg', 'rb')as fin:
                            r = fin.read(block_size)
                            while r:
                                self.request.send(r)
                                r = fin.read(block_size)
                    else:
                        print("cmd", operation)
                        # fixbug：client发送数据时，多个指令重合
                        opers = operation.split("_")
                        for oper in opers:
                            if oper:
                                my_car.exec_operation(int(operation))
                else:
                    print("empty cmd")
                    break
            except TimeoutError:
                print("a client quited")
                break

if __name__ == '__main__':
    server = None
    my_car = None
    try:
        cf = read_config()
        my_car = Car(cf)
        cam = CamMotion(cf['cam_server_ip']['ip'], cf['cam_server_ip']['control_port'])
        cam.check()
        server = TCPServer(('', 8001), ResponseHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        my_car.disconnect()
        server.server_close()
