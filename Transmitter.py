import socket, struct, time, struct
import utils
from SlidingWindow import SlidingWindow

class Transmitter:  
    '''
    This class represents the transmitter.
    '''

    def __init__(self, window_size):
        # self.sws = window_size  #upper bound on the number of frames that can be trasmitted
        # self.lar = 0    #seq num of the last ack received
        # self.lfs = 0    #seq num of the last frame sent
        self.window = SlidingWindow(window_size)

        self.messages = 0   #stores the amount of different messages sent
        self.messages_sent = 0  #stores the amount of messages sent - includes retrasnmition
        self.incorrect_messages = 0 #stores the amout of messages sent with incorrect md5

        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def hello(self):
        print('Hello')

    def mount_packet(self, sequence_number, message, error):
        error_code = None

        period = time.time()
        seconds = int(period)
        nanoseconds = int(str(period).split('.')[1])
        message_size = len(bytes(message, 'utf-8'))

        if (error):
            error_code = utils.generate_md5(['Message with error'])
            print('Message generated with incorrect MD5, seq_no = ' + str(sequence_number))
        else:
            error_code = utils.generate_md5([sequence_number, seconds, nanoseconds, message_size, message])
            print('Message generated with correct MD5, seq_no = ' + str(sequence_number))
        
        pack_format = '!Q Q L H ' + str(message_size) + 's' + str(len(error_code)) + 's'

        packet = struct.pack(pack_format, sequence_number, seconds, nanoseconds, message_size, bytes(message, 'utf-8'), error_code)

        return packet
        # unpacked = struct.unpack(pack_format, packet)
        # print(unpacked[-2].decode("utf-8"))

