import socket
import threading
import xml.etree.ElementTree as ET
import xmlschema



class UDPServer:
    def __init__(self, parser_fn, schema_path=None, host='127.0.0.1', port=0):
        """
        Initialize a UDP server with optional XML schema and custom parser.

        :param parser_fn: Function to parse incoming data: parser_fn(data: bytes) -> dict | None
        :param schema_path: Path to optional XSD schema for validation
        """
        self.host = host
        self.port = port
        self.parser_fn = parser_fn
        self.schema = xmlschema.XMLSchema(schema_path) if schema_path else None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))
        self.port = self.sock.getsockname()[1]

        self.running = False
        self.clients = {}  # addr -> player data
        self.handlers = []  # handler(player_data, addr, shutdown)

    def add_handler(self, handler_fn):
        self.handlers.append(handler_fn)

    def _validate(self, data: bytes):
        if not self.schema:
            return True
        try:
            root = ET.fromstring(data.decode('utf-8'))
            self.schema.validate(root)
            return True
        except Exception as e:
            print(f"[UDP_SERVER]: <XML_VALIDATE> ~ Schema validation failed: {e}")
            return False

    def _handle_client(self, data, addr, shutdown=False):
        player_data = None

        if not shutdown:
            if not self._validate(data):
                return

            player_data = self.parser_fn(data)
            if not player_data:
                print(f"[UDP_SERVER]: Parse failed from {addr}")
                return

            self.clients[addr] = player_data
        else:
            player_data = self.clients.get(addr)

        for handler in self.handlers:
            try:
                response = handler(player_data, addr, shutdown)
                if response:
                    self.sock.sendto(response, addr)
            except Exception as e:
                print(f"[UDP_SERVER]: Handler error from {addr}: {e}")

    def _listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                threading.Thread(target=self._handle_client, args=(data, addr), daemon=True).start()
            except Exception as e:
                print(f"[UDP_SERVER]: Listen error: {e}")

    def start(self):
        self.running = True
        threading.Thread(target=self._listen, daemon=True).start()
        print(f"[UDP_SERVER]: Running on {self.host}:{self.port}")

    def stop(self):
        self.running = False
        print("[UDP_SERVER]: Stopping...")
        for addr in self.clients:
            try:
                self._handle_client(b'', addr, shutdown=True)
            except Exception as e:
                print(f"[UDP_SERVER]: Shutdown notice failed to {addr}: {e}")
        self.sock.close()
