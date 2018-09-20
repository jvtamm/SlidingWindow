import socket
from sys import argv
from Receiver import Receiver


def main(argv):
    print('I\'m main')
    print(argv)

    # Should initialize a Receiver with window size
    receiver = Receiver(argv[3])

    # Should bind to address
    # Should listen to 10 
    receiver.udp.bind((socket.gethostname(),int(argv[2])))

    print(vars(receiver))

    # Enter a while true loop
    while(True):
        print('Waiting')
    # Keep on waiting for requests with function accept and get transmitter address
    # Check tranmitter address in list
        # If it is already in the list, check if frame is in sliding window range:
            # If it is and is the next to be written in the file just write and send ack else just insert in the siding window and send ack
            #  Else just ignore
        # Else create new client and perform exactly the same tasks


if __name__ == '__main__':
    main(argv)