import RPi.GPIO as GPIO
from collections import OrderedDict


class Car:
    """小车的控制部分，TODO：更多拐弯的方式"""

    def __init__(self, cf):
        # 这样生成的字典中元素按照插入的顺序排列
        self.out_mapping_port = OrderedDict()
        self.read_config(cf)
        self.stand_order = ['f_out1', 'f_out2', 'f_out3', 'f_out4']

    def read_config(self, cf):
        """读取配置文件映射端口"""

        if int(cf['front_engine']['out1']) != 0:
            # 读入的配置中，每个section中应该是有序的吧？？？？不然ordereddict也就没用了。
            for key in cf['front_engine']:
                self.out_mapping_port['f_' + key] = int(cf['front_engine'][key])
        if int(cf['rear_engine']['out1']) != 0:
            for key in cf['rear_engine']:
                self.out_mapping_port['r_' + key] = int(cf['rear_engine'][key])
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        for key in self.out_mapping_port:
            GPIO.setup(self.out_mapping_port[key], GPIO.OUT)

    def exec_operation(self, operation):
        """operation按照二进制位对应r_4,3,2,1 f_4,3,2,1前驱后驱的out端口"""
        for key in self.out_mapping_port:
            print(key)
            GPIO.output(self.out_mapping_port[key], operation & 1)
            operation >>= 1

    def disconnect(self):
        # 清除针脚的状态，有点类似读写文件时的close
        GPIO.cleanup()

    # TODO: 是否需要检查下
    # 下面的相当于是二驱的模式进行控制
    def forward(self):
        self.exec_operation(self, 0b01100110)

    def back(self):
        self.exec_operation(self, 0b10011001)

    def stop(self):
        self.exec_operation(self, 0b00000000)

    def front_left(self):
        self.exec_operation(self, 0b00100010)

    def front_right(self):
        self.exec_operation(self, 0b01000100)

    def back_left(self):
        self.exec_operation(self, 0b00010001)

    def back_right(self):
        self.exec_operation(self, 0b10001000)
