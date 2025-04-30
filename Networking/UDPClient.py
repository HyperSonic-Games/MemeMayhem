import socket
import xmlschema
from .. import Config
from .. import Utils
import xml.etree.ElementTree as ET


class UDPClient:
    def __init__(self, schema_path, server_host='127.0.0.1', server_port=12345):
        """Initialize the UDP client and load XML schema."""
        self.pm = Utils.PopupManager()
        self.server = (server_host, server_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5)
        self.schema = xmlschema.XMLSchema(schema_path)

    def send(self, message: bytes):
        """Send a validated XML message to the server, receive and validate XML response."""
        try:
            # Outgoing XML validation
            outgoing_xml = message.decode('utf-8')
            outgoing_element = ET.fromstring(outgoing_xml)
            self.schema.validate(outgoing_element)

            if Config.DEV_MODE:
                print("[MEME_MAYHEM/UDP_CLIENT]: <OUTGOING_XML_VALIDATED> ✓")
                print(f"[MEME_MAYHEM/UDP_CLIENT]: <SENT_MSG> ~ \n{outgoing_xml}")


        except (ET.ParseError, xmlschema.XMLSchemaException) as e:
            if Config.DEV_MODE:
                print(f"[MEME_MAYHEM/UDP_CLIENT]: <INVALID_OUTGOING_XML> ✗\nError: {e}")
            else:
                self.pm.Error("[MEME_MAYHEM/UDP_CLIENT]", f"<INVALID_OUTGOING_XML> ~ ✗\nError: {e}")
            return None

        try:
            self.sock.sendto(message, self.server)

            data, _ = self.sock.recvfrom(4096)
            xml_data = data.decode('utf-8')

            if Config.DEV_MODE:
                print(f"[MEME_MAYHEM/UDP_CLIENT]: <RECEIVED_RAW> ~ \n{xml_data}")

            try:
                incoming_element = ET.fromstring(xml_data)
                self.schema.validate(incoming_element)

                if Config.DEV_MODE:
                    print("[MEME_MAYHEM/UDP_CLIENT]: <INCOMING_XML_VALIDATED> ✓")

                return incoming_element

            except (ET.ParseError, xmlschema.XMLSchemaException) as e:
                if Config.DEV_MODE:
                    print(f"[MEME_MAYHEM/UDP_CLIENT]: <INVALID_INCOMING_XML> ✗\nError: {e}")
                else:
                    self.pm.Error("MEME_MAYHEM/UDP_CLIENT", f"<INVALID_INCOMING_XML> ✗\nError: {e}")
                return None

        except socket.timeout:
            if Config.DEV_MODE:
                print("[MEME_MAYHEM/UDP_CLIENT]: <RECEIVE_TIMEOUT> Response from server timed out")
            return None

        except Exception as e:
            if Config.DEV_MODE:
                print(f"[MEME_MAYHEM/UDP_CLIENT]: <UNEXPECTED_ERROR> ⚠\nError: {e}")
            else:
                self.pm.Error("MEME_MAYHEM/UDP_CLIENT", f"<UNEXPECTED_ERROR> ⚠\nError: {e}")
            return None

    def close(self):
        """Close the UDP socket."""
        self.sock.close()
