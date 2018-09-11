import struct
from sys import argv
from Transmitter import Transmitter

if __name__ == '__main__':
    transmitter = Transmitter(argv[3], argv[4], argv[5])

    """Connect to socket"""
    ip, port = argv[2].split(':')
    transmitter.udp.connect((ip, int(port)))

    with open(argv[1]) as fp:
        sequence_number = 0
        for line in fp:
            packet = transmitter.mount_package(sequence_number, line.split('\n')[0])
            sequence_number += 1