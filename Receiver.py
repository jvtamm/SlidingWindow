import socket, struct, time, struct, sys, binascii
from threading import Lock
import utils
from ServerClient import Client

class Receiver:
    def __init__(self, window_size, p_error):
        # Instanciate a client list
        self.client_list = []
        self.window_size = window_size
        self.p_error = p_error
        self.lock = Lock()
        
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def handle_message(self):
        message, address = self.udp.recvfrom(65573)
        unpacked = struct.unpack('!Q Q L H', message[0:22])
        message_end = 22 + unpacked[3]
        message_body = message[22:message_end].decode('ascii')
        
        self.lock.acquire()

        client = self.find_client_in_list(address)
        if(client == None):
            # print('Client not in list')
            client = self.create_client_in_list(address)

        if (utils.check_md5(message[0:message_end], message[message_end: 38 + message_end])):
            if(unpacked[0] < client.window.buffer[0].sequence_number):
                # print('resend ack, seq_num:' + str(unpacked[0]))
                self.handle_ack(unpacked[0], address)
            elif(unpacked[0] > client.window.buffer[-1].sequence_number):
                # print('Ignore, out of window, seq_num: ' + str(unpacked[0]))
                status = 'Out of window'
            else:
                # print('Sending ack to: ' + str(unpacked[0]))
                client.save_message(message_body, unpacked[0])
                self.handle_ack(unpacked[0], address)      
        # else:
        #     print('Ignore, md5 is wrong, seq_num:' + str(unpacked[0]))

        self.lock.release()
        
        return client

    def handle_ack(self, sequence_number, address):
        period = time.time()
        seconds = int(period)
        nanoseconds = int((period - seconds) * (10**9))

        ack = struct.pack('! Q Q L', sequence_number, seconds, nanoseconds)


        md5 = utils.generate_md5(ack)
        if (utils.compare_error(self.p_error)):
            # print('Ack send with wrong md5, seq_num:' + str(sequence_number))
            md5 = utils.corrupt_md5(md5)
        
        sent = self.udp.sendto(ack + md5, address)
        if sent == 0:
            raise RuntimeError("Failed to send the ack")

    
    def find_client_in_list(self, address):
        # self.lock.acquire()

        for client in self.client_list:
            if(client.address == address):
                # self.lock.release()
                return client

        # self.lock.release()
        return None
    
    def create_client_in_list(self, address):
        # print('Inserting client in list...')
        client = Client(self.window_size, address)
        # self.lock.acquire()
        self.client_list.append(client)
        # self.lock.release()
        
        return client
        

        

