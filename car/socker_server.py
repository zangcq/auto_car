"""socketserver在小车端，因为要控制小车的运动，是pc向小车发送指令"""
from socketserver import BaseRequestHandler, TCPServer
from Car import Car

my_car = Car()


class ResponseHandler(BaseRequestHandler):
    global my_car

    def handle(self):
        self.request.settimeout(3)
        while True:
            # 接收控制指令。与客户端约定好mapping
            operation = self.request.recv(8192).strip()
            if operation:
                print(operation)
                my_car.exec_operation(int(operation))


if __name__ == '__main__':
    try:
        server = TCPServer(('', 8000), ResponseHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        my_car.disconnect()
        server.server_close()
