import RPi.GPIO as GPIO
import configparser
# TODO:最后提取配置
class Car:
    def __init__(self):
        self.out_mapping_port = dict()
        self.read_config()

    def read_config(self):
        """读取配置文件映射端口"""
        cf = configparser.ConfigParser()
        cf.read('config.ini')
        if int(cf['front_engine']['out1']) != 0:
            for key in cf['front_engine']:
                self.out_mapping_port['f_' + key] = int(cf['front_engine'])
        if int(cf['rear_engine']['out1']) != 0:
            for key in cf['rear_engine']:
                self.out_mapping_port['r_' + key] = int(cf['rear_engine'])




GPIO.cleanup()
# 设置模式为BCM模式，在前面的文章中已经说明过几种模式的不同
GPIO.setmode(GPIO.BCM)
# 设置26号的模式为输出模式，即系统向26写数据
GPIO.setup(OUT1_H, GPIO.OUT)
GPIO.setup(OUT2_H, GPIO.OUT)
GPIO.setup(OUT3_H, GPIO.OUT)
GPIO.setup(OUT4_H, GPIO.OUT)
def move_forward():

try:
    # 输出数据1,即置26针脚为高电平
    GPIO.output(OUT1_H, 0)
    GPIO.output(OUT2_H, 1)
    GPIO.output(OUT3_H, 1)
    GPIO.output(OUT4_H, 0)

except KeyboardInterrupt:
    # 清除针脚的状态，有点类似读写文件时的close
    GPIO.cleanup()
