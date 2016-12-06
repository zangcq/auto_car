"""socketserver在小车端，因为要控制小车的运动，是pc向小车发送指令"""
from socketserver import BaseRequestHandler, TCPServer


class ResponseHandler(BaseRequestHandler):
    def handle(self):
        while True:
            # 接收控制指令
            operation = self.request.recv(8192)
            car.oper(operation)


if __name__ == '__main__':
    server = TCPServer(('', 8000), ResponseHandler)
    server.serve_forever()