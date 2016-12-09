from socket import socket, AF_INET, SOCK_STREAM
from evdev import InputDevice, categorize, ecodes
from time import sleep
import configparser


s = socket(AF_INET, SOCK_STREAM)
# 对应的十进制z34，68，153，0，102
key_code = {ecodes.KEY_UP: 0b01100110, ecodes.KEY_DOWN: 0b10011001, ecodes.KEY_LEFT:0b00100010, ecodes.KEY_RIGHT:0b01000100, ecodes.KEY_SPACE: 0b00000000}


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



def key_monitor():
    dev = InputDevice('/dev/input/event4')
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            # print(event.code, event.type, event.value)
            if event.code in [ecodes.KEY_UP, ecodes.KEY_DOWN, ecodes.KEY_LEFT, ecodes.KEY_RIGHT, ecodes.KEY_SPACE]:
                if event.value == 1:
                    print(event.code, 'is down')
                elif event.value == 2:
                    print(event.code, "is pressed")
                    # 先测试只有在按住的时候，才发送数据
                    s.send(bytes(str(key_code[event.code]), "utf-8"))
                else:
                    print(event.code, "is up")

try:
    init()
    # key_monitor()
except KeyboardInterrupt:
    s.close()