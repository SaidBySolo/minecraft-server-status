from contextlib import suppress
import json
from dns import resolver
from dns.rdtypes.IN.SRV import SRV
from socket import socket, AF_INET, SOCK_STREAM

SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80


def read_varint(data: bytes, offset: int) -> tuple[int, int]:
    value = 0
    shift = 0
    while True:
        byte = data[offset]
        value |= (byte & SEGMENT_BITS) << shift
        offset += 1
        if not byte & CONTINUE_BIT:
            break
        shift += 7
    return value, offset


def write_varint(value: int) -> bytes:
    result = bytearray()
    while True:
        byte = value & SEGMENT_BITS
        value >>= 7
        if value:
            byte |= CONTINUE_BIT
        result.append(byte)
        if not value:
            break
    return bytes(result)


class Resolver:
    def __init__(self, host: str, port: int = 25565):
        self.host = host
        self.port = port
        with suppress(resolver.NoAnswer):
            srv = self._get_srv_record()
            self.host = srv[0]
            self.port = srv[1]

    def _get_srv_record(self):
        resolved = resolver.resolve("_minecraft._tcp." + self.host, "SRV")
        answers = resolved.response.answer
        if answers:
            answer = answers[0]
            for rdata in answer:
                if isinstance(rdata, SRV):
                    return rdata.target.to_text()[:-1], rdata.port

    def check_server(self):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))

            packet_id = write_varint(0)
            protocol_version = write_varint(770)
            server_address = self.host.encode("utf-8")
            server_port = self.port.to_bytes(2, "big")
            status = write_varint(1)

            handshake_data = (
                packet_id
                + protocol_version
                + write_varint(len(server_address))
                + server_address
                + server_port
                + status
            )
            # Handshake
            sock.send(write_varint(len(handshake_data)) + handshake_data)
            # Status Request
            sock.send(write_varint(len(packet_id)) + packet_id)
            # Read full response
            length, _ = read_varint(sock.recv(5), 0)  # Read the length of the response
            response = sock.recv(length).decode("utf-8")  # Read the full response
            return json.loads(response)  # Parse the JSON response
