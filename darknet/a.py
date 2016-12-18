from time import sleep
import os
from multiprocessing import Process
import subprocess
darknet_path_root = '/home/find/Dropbox/github/auto_car/darknet/'
def control_cmd(input_file):
    """:return left, right , forward"""
    # p = subprocess.check_output('%s/darknet yolo test %s/tiny-yolo.cfg %stiny-yolo.weights %s' % (darknet_path_root, darknet_path_root, darknet_path_root, input_file))
    input_args = ['/home/find/Dropbox/github/auto_car/darknet//darknet', 'yolo', 'test', '/home/find/Dropbox/github/auto_car/darknet//tiny-yolo.cfg', '/home/find/Dropbox/github/auto_car/darknet/tiny-yolo.weights', 'test.jpg']

    p = subprocess.check_output( input_args)
    p = p.decode('utf8')
    # p = os.popen('%s/darknet yolo test %s/tiny-yolo.cfg %stiny-yolo.weights %s' % (
    #     darknet_path_root, darknet_path_root, darknet_path_root, input_file), 'r')
    # line = p.readline()
    # print('direction', line)
    print("cmd", p)
def work():
	control_cmd('test.jpg')
p = Process(target=work)
p.start()