import os.path
from socket import socket, AF_INET, SOCK_STREAM
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import configparser
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
pi_ip = ''


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class CameraHadler(tornado.web.RequestHandler):
    def get(self):
        self.render("cam.html", pi_ip=pi_ip)
        # def post(self):
        #     source_text = self.get_argument('source')
        #     text_to_change = self.get_argument('change')
        #     change_lines = text_to_change.split('\r\n')
        #     self.render('munged.html', source_map=source_map, change_lines=change_lines,
        #                 choice=random.choice)


class ControlSocket:
    def __init__(self, socket_ip):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect(socket_ip, 8001)
        self.socket.sendall(bytes('start', "utf-8"))
        self.block_size = 2048

    def get_pic(self, file_name):
        """从socket接收到文件，并写入本地文件"""
        file_size = self.socket.recv(self.block_size)
        recv_data_size = 0
        data = b''
        with open(file_name, 'wb') as fout:
            while recv_data_size < file_size:
                data = self.socket.recv(self.block_size)
                fout.write(data)
                recv_data_size += len(data)
                # print(recv_data_size)

    def work(self):
        pass

if __name__ == '__main__':
    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    pi_ip = cf['pi_ip']['ip']



    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/', IndexHandler), (r'/cam', CameraHadler)],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
