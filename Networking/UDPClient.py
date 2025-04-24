import socket

class UDPClient:
    def __init__(self, server_host='127.0.0.1', server_port=12345):
        self.server = (server_host, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5)

    def send(self, message: bytes):
        self.sock.sendto(message, self.server)
        try:
            data, _ = self.sock.recvfrom(4096)
            return data
        except socket.timeout:
            return None

    def close(self):
        self.sock.close()
