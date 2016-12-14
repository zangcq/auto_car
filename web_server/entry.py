import os.path
from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
import random
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import configparser
from tornado.options import define, options
import subprocess

define("port", default=8000, help="run on the given port", type=int)
pi_ip = ''
darknet_path_root = ''
# 对应的十进制z34，68，153，0，102
direction_code = {'forward': 0b01100110, 'backward': 0b10011001, 'left': 0b00100010, 'right': 0b01000100,
                  'stop': 0b00000000}


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
        """"""
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((socket_ip, 8001))
        self.socket.sendall(bytes('start', "utf-8"))
        self.block_size = 2048

    def get_pic(self, file_name):
        """从socket接收到文件，并写入本地文件"""
        file_size = int(self.socket.recv(self.block_size))
        recv_data_size = 0
        data = b''
        with open(file_name, 'wb') as fout:
            while recv_data_size < file_size:
                data = self.socket.recv(self.block_size)
                fout.write(data)
                recv_data_size += len(data)
                # print(recv_data_size)

    def move(self, direction):
        """发送对应的方向指令给小车"""
        print(direction)
        print(str(direction_code[direction]))
        self.socket.sendall(bytes(str(direction_code[direction]), 'utf8'))


def control_cmd(input_file):
    """:return left, right , forward"""
    # p = os.popen('%s/darknet yolo test %s/tiny-yolo.cfg %stiny-yolo.weights %s' % (
    #     darknet_path_root, darknet_path_root, darknet_path_root, input_file), 'r')
    # line = p.readline()
    # print('direction', line)
    # return line
    print('try')
    input_args = ["%sdarknet" % darknet_path_root, 'yolo', 'test', '%stiny-yolo.cfg' % darknet_path_root,
                  '%stiny-yolo.weights' % darknet_path_root, input_file]
    print(input_args)
    p = subprocess.check_output(input_args)
    p = p.decode('utf8')
    print("cmd ", p)

    # p = subprocess.Popen(input_args, stdout=subprocess.PIPE)
    # p.wait()
    # print(p.stdout.read())
    return p


def socket_work(c_socket):
    c_socket.get_pic('test.jpg')
    c_socket.move(control_cmd('test.jpg'))


if __name__ == '__main__':
    # 读取配置文件
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    pi_ip = cf['pi_ip']['ip']
    # darknet的运行目录
    darknet_path_root = cf['darknet']['darknet_path_root']

    c_socket = ControlSocket(pi_ip)
    # 通过socket控制小车的进程
    socket_process = Process(target=socket_work, args=(c_socket,))
    socket_process.start()

    # tornado.options.parse_command_line()
    # app = tornado.web.Application(
    #     handlers=[(r'/', IndexHandler), (r'/cam', CameraHadler)],
    #     template_path=os.path.join(os.path.dirname(__file__), "templates"),
    #     static_path=os.path.join(os.path.dirname(__file__), "static"),
    #     debug=True
    # )
    # http_server = tornado.httpserver.HTTPServer(app)
    # http_server.listen(options.port)
    # tornado.ioloop.IOLoop.instance().start()
