import socket, struct, time, struct, sys, binascii

class Receiver:
    def __init__(self, window_size):
        # Instanciate a client list
        
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
