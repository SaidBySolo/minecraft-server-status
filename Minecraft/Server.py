import dns.resolver
import socket


class HostInfo:
    def __init__(self, host, port, ip):
        self.host = host
        self.port = port
        self.ip = ip

    @staticmethod
    def get_hostinfo(address):
        try:
            all_response = dns.resolver.query("_minecraft._tcp." + address, "SRV")
            response = all_response[0]
        except Exception as e:
            print(f"Unexpected Error: {e}")
        else:
            host = str(response.target).rstrip(".")
            port = int(response.port)
            ip = socket.gethostbyname(host)

        return HostInfo(host, port, ip)
