import struct
import zlib
import base64
import json
from typing import Any

class Serializer:
    @staticmethod
    def serialize(data: Any) -> bytes:
        """
        Serializes the given data into a compact binary format using base64 encoding,
        and appends a CRC32 checksum.
        """
        json_data = json.dumps(data)
        encoded_data = json_data.encode('utf-8')
        compressed_data = base64.b64encode(encoded_data)
        checksum = zlib.crc32(compressed_data)  # Compute CRC32 checksum
        return struct.pack(f'!I{len(compressed_data)}s', checksum, compressed_data)

    @staticmethod
    def deserialize(packet: bytes) -> Any:
        """
        Deserializes the given byte packet, verifies its checksum,
        and returns the original data.
        """
        if len(packet) < 4:
            raise ValueError("Invalid packet: too short")

        checksum, compressed_data = struct.unpack(f'!I{len(packet) - 4}s', packet)
        
        if zlib.crc32(compressed_data) != checksum:
            raise ValueError("Checksum mismatch: data corrupted")
        
        encoded_data = base64.b64decode(compressed_data)
        return json.loads(encoded_data.decode('utf-8'))

