import socket, struct, time, struct, sys, binascii
from copy import deepcopy
import utils
from ClientSlidingWindow import SlidingWindow

class Transmitter:  
    '''
    This class represents the transmitter.
    '''

    def __init__(self, window_size, p_error, timeout, host, port):
        self.window = SlidingWindow(window_size)
        self.p_error = p_error
        self.timeout = timeout
        self.address = (host, port)

        self.messages = 0   #stores the amount of different messages sent
        self.messages_sent = 0  #stores the amount of messages sent - includes retrasnmition
        self.incorrect_messages = 0 #stores the amout of messages sent with incorrect md5

        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def mount_packet(self, sequence_number, message):
        period = time.time()
        seconds = int(period)
        nanoseconds = int((period - seconds) * (10**9))
        message_size = len(bytes(message, 'ascii'))

        pack_format = '!Q Q L H '
        packet = struct.pack(pack_format, sequence_number, seconds, nanoseconds, message_size)
        packet += bytes(message, 'ascii')

        error_code = utils.generate_md5(packet)
        
        return packet + error_code
    
    def send_packet(self, packet):
        unpacked = struct.unpack('!Q', packet[0:8])
        # print('Sending packet: ' + str(unpacked[0]))

        sent = self.udp.sendto(packet, self.address)
        if sent == 0:
            raise RuntimeError("Failed to send the packet")
        
        self.messages += 1
        self.messages_sent += 1


    def resend_packet(self, element):
        # print('Resending packet: ' + str(element.sequence_number))

        if(element.ack): 
            return
            
        packet = deepcopy(element.packet)
        if (utils.compare_error(self.p_error)):
            packet = utils.corrupt_md5(packet)
            self.incorrect_messages += 1
        
        sent = self.udp.sendto(packet, self.address)
        if sent == 0:
            raise RuntimeError("Failed to send the packet")
        
        element.reset_timer(self.timeout, self.resend_packet)
        self.messages_sent += 1
    
    def handle_ack(self):
        ack = self.udp.recv(36)
        unpacked = struct.unpack('! Q Q L', ack[0:20])

        element = self.window.find_in_list(unpacked[0])
        if (element != None):
            if (utils.check_md5(ack[0:20], ack[20:36])):
                # print('Received ack: ' + str(unpacked[0]))
                element.set_ack()
            else:
                self.resend_packet(element)
        

