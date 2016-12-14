import os
from multiprocessing import Process
import subprocess
darknet_path_root = '/home/find/Dropbox/github/auto_car/darknet/'
def control_cmd(input_file):
    """:return left, right , forward"""
    # p = subprocess.check_output('%s/darknet yolo test %s/tiny-yolo.cfg %stiny-yolo.weights %s' % (darknet_path_root, darknet_path_root, darknet_path_root, input_file))
    p = subprocess.check_output( ['%s/darknet' % darknet_path_root,'yolo','test','%s/tiny-yolo.cfg' % darknet_path_root, '%stiny-yolo.weights' % darknet_path_root, input_file])
    p = p.decode('utf8')
    # p = os.popen('%s/darknet yolo test %s/tiny-yolo.cfg %stiny-yolo.weights %s' % (
    #     darknet_path_root, darknet_path_root, darknet_path_root, input_file), 'r')
    # line = p.readline()
    # print('direction', line)
    print(p)
def work():
	control_cmd('test.jpg')
p = Process(target=work)
p.start()