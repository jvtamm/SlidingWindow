import socket
from sys import argv
from Receiver import Receiver


def main(argv):
    # Should initialize a Receiver with window size
    receiver = Receiver(int(argv[3]), float(argv[4]))

    # Should bind to address
    # Should listen to 10 
    receiver.udp.bind(('',int(argv[2])))

    # Enter a while true loop
    while(True):
        # print('Waiting')
    # Keep on waiting for requests with function accept and get transmitter address
        client = receiver.handle_message()
    # Check tranmitter address in list
        # If it is already in the list, check if frame is in sliding window range:
            # If it is insert in the siding window and send ack
            #  Else just ignore
        # Else create new client and perform exactly the same tasks
    
    # Iterate over client window writing all messages in order in the file until first empty position. Slide window accordingly
        # print('Printing now...')
        # client.print_window()
        position = 0

        receiver.lock.acquire()

        iterator = client.window.buffer[position]
        while(iterator.message != None):
            with open(argv[1], "a") as output:
                # client.print_window()
                # print()
                output.write(iterator.message + '\n')
            
            # Should slide window
            position += 1
            try:
                iterator = client.window.buffer[position]
            except:
                break
        
        client.window.slide_window(position)

        receiver.lock.release()

if __name__ == '__main__':
    main(argv)
