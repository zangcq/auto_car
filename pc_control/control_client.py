from socket import socket, AF_INET, SOCK_STREAM
from evdev import InputDevice, categorize, ecodes
from time import sleep
import configparser

s = socket(AF_INET, SOCK_STREAM)
# 对应的十进制z34，68，153，0，102
key_code = {ecodes.KEY_UP: 0b10010110, ecodes.KEY_DOWN: 0b01101001, ecodes.KEY_LEFT: 0b10100101,
            ecodes.KEY_RIGHT: 0b01011010, ecodes.KEY_SPACE: 0b00000000, 'left_rotate_90': 0b10100101}


def init():
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    s.connect((cf['server_ip']['ip'], int(cf['server_ip']['port'])))
    s.sendall(bytes('start', "utf-8"))
    block_size = 2048
    file_size = int(s.recv(block_size))
    print(file_size)
    recv_data_size = 0
    data = b''
    with open('/home/find/ddown/test.jpg', 'wb') as fout:
        while recv_data_size < file_size:
            data = s.recv(block_size)
            fout.write(data)
            recv_data_size += len(data)
            print(recv_data_size)


def formulate_operation(oper):
    """发现bug：socket传输数据的时候，会将发送的数字指令重叠在一起发送，此函数将加入特殊标记，在server端根据这个特殊分隔符处理。"""
    return "_%d_" % oper


def key_monitor():
    dev = InputDevice('/dev/input/event4')
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            # print(event.code, event.type, event.value)
            if event.code in [ecodes.KEY_UP, ecodes.KEY_DOWN, ecodes.KEY_LEFT, ecodes.KEY_RIGHT, ecodes.KEY_SPACE]:
                if event.value == 1:
                    # 1表示按下
                    print(event.code, 'is down')
                    if event.code in[ecodes.KEY_LEFT, ecodes.KEY_RIGHT]:
                        s.send(bytes(formulate_operation(key_code[event.code]), "utf-8"))
                        sleep(0.15)
                        s.send(bytes(formulate_operation(key_code[ecodes.KEY_SPACE]), 'utf8'))
                elif event.value == 2:
                    # 2表示按住了
                    print(event.code, "is pressed")
                    if event.code == ecodes.KEY_LEFT or event.code == ecodes.KEY_RIGHT:
                        pass
                    # 先测试只有在按住的时候，才发送数据
                    s.send(bytes(formulate_operation(key_code[event.code]), "utf-8"))
                else:
                    print(event.code, "is up")


try:
    init()
    key_monitor()
except KeyboardInterrupt:
    s.close()
