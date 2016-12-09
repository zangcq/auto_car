from socket import socket, AF_INET, SOCK_STREAM
from evdev import InputDevice, categorize, ecodes
from time import sleep
import configparser


s = socket(AF_INET, SOCK_STREAM)

key_code = {ecodes.KEY_UP: 0b01100110, ecodes.KEY_DOWN: 0b10011001, ecodes.KEY_LEFT:0b00100010, ecodes.KEY_RIGHT:0b01000100, ecodes.KEY_SPACE: 0b00000000}


def init():
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    s.connect((cf['server_ip']['ip'], int(cf['server_ip']['port'])))

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
    key_monitor()
except KeyboardInterrupt:
    s.close()