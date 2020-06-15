import socket
from Server import HostInfo

info = HostInfo.get_hostinfo("hostname")
ip = info.ip
port = info.port

client_socket = socket.socket()