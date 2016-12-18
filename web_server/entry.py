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

def switch_block(left, right, l_border, r_border):
    """检测边界位于哪个block"""
    if right <= l_border:
        return 1
    if right <= r_border:
        if left >= l_border:
            return 2
        else:
            return 3
    else:
        if left >= r_border:
            return 4
        elif left >= l_border:
            return 6
        else:
            return 7

def judge_barriers_1(barriers_in_block, target_in_block, block1, block2, direction1, direction2, direction3):
    if barriers_in_block[target_in_block]:
        if not barriers_in_block[block1]: return direction1, False, True
        if not barriers_in_block[block2]: return direction2, False, True
        return 'cannot', False, False
    else:
        return direction3, False, True

def judge_barriers_2(barriers_in_block, block2, block3, direction1, direction2):
    if barriers_in_block[2]:
        if barriers_in_block[block2]:
            if barriers_in_block[block3]:
                return 'cannot', False, False
            else:
                return direction1, False, True
        else:
            return direction2, False, True
    else:
        return 'forward', False, True

def control_cmd(global_direction):
    """
    发送控制指令
    :param global_direction:累计在全局方向上转了多少次，正数表示右转的次数，负数表示左转的次数
    :return:方向, 是否需要拍照， 是否前行
    """
    p = subprocess.check_output(['./darknet', 'yolo', 'test', './cfg/tiny-yolo.cfg',
                                './tiny-yolo.weights', './data/5.jpg'])
    item_list = p.strip().splitlines()
    image_width = int(item_list[0])
    right_border = image_width * 2 / 3
    left_border = image_width / 3
    target_name = 'person'
    barrier_name = 'bottle'
    # block编号： 1,2,4,如果出现横跨，则取和
    # 内部元素分别是：所在的block
    target_in_block = 0
    # 一共三个block，每个block上是否有障碍物
    barriers_in_block = [False for _ in range(9)]
    stand_turn_direction = {True:'right', False:'left'}
    # 分类输出的结果
    for item in item_list:
        item = item.split(',')
        if item[0] == target_name:
            # target_info = item[1:]
            target_in_block = switch_block(int(item[1]), int(item[2]), left_border, right_border)
        elif item[0] == barrier_name:
            barriers_in_block[int(switch_block(int(item[1]), int(item[2]), left_border, right_border))] = True
    if barriers_in_block[3]:
        barriers_in_block[1] = barriers_in_block[2] = True
    if barriers_in_block[6]:
        barriers_in_block[2] = barriers_in_block[4] = True
    if barriers_in_block[7]:
        barriers_in_block = [True for _ in range(9)]

    if target_in_block:
        if target_in_block == 7:
            return 'finish', False, False
        if target_in_block in [1, 2, 4]:
            if target_in_block == 2:
                return judge_barriers_1(barriers_in_block, target_in_block, 1, 4, 'left', 'right', 'forward')
            elif target_in_block == 4:
                return judge_barriers_1(barriers_in_block, target_in_block, 2, 1, 'forward', 'left', 'right')
            else:  return judge_barriers_1(barriers_in_block, target_in_block, 2, 4, 'forward', 'right', 'left')
        elif target_in_block == 3:
            judge_barriers_2(barriers_in_block,  1, 4, 'right', 'left')
        else:
            judge_barriers_2(barriers_in_block,  4, 1, 'left', 'right')
    else:
        # 目标不在视野范围内,则调整角度，重新拍照
        # 注意global要减
        return stand_turn_direction[global_direction < 0], True, False



def socket_work(c_socket):
    c_socket.get_pic('test.jpg')




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
