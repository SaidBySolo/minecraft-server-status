import dns.resolver
import socket


class HostInfo:
    def __init__(self):
        self.host = host
        self.port = port

    def get_hostinfo(self, address):
        try:
            all_response = dns.resolver.query(
                "_minecraft._tcp." + address, "SRV")
            response = all_response[0]
            host = str(response.target).rstrip(".")
            port = int(response.port)

        except Exception as e:
            print(f"Unexpected Error: {e}")

        return HostInfo(host, port)
