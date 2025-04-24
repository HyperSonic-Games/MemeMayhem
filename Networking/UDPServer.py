import socket
import threading

class UDPServer:
    def __init__(self, host='127.0.0.1', port=0):
        self.host = host
        self.port = port
        self.handlers = []
        self.running = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.port = self.sock.getsockname()[1]  # Get assigned port

    def add_handler(self, handler):
        """Add a handler with signature: handler(data: bytes, addr: tuple) -> response_bytes"""
        self.handlers.append(handler)

    def _handle_client(self, data, addr):
        for handler in self.handlers:
            response = handler(data, addr)
            if response:
                self.sock.sendto(response, addr)

    def _listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                threading.Thread(target=self._handle_client, args=(data, addr), daemon=True).start()
            except Exception as e:
                print(f"Server error: {e}")

    def start(self):
        self.running = True
        threading.Thread(target=self._listen, daemon=True).start()
        print(f"UDP Server running on {self.host}:{self.port}")

    def stop(self):
        self.running = False
        self.sock.close()
