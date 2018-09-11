import socket, struct, time, struct
import utils

class Transmitter:
    '''
    This class represents the transmitter.
    '''

    def __init__(self, window_size, timeout, p_error):
        self.sws = window_size  #upper bound on the number of frames that can be trasmitted
        self.lar = 0    #seq num of the last ack received
        self.lfs = 0    #seq num of the last frame sent
        self.window_buffer = []
        self.timeout = timeout  #max amount of time that can be waited for an ack
        self.p_error = p_error  #denotes the probability of the message being corrupted

        self.messages = 0   #stores the amount of different messages sent
        self.messages_sent = 0  #stores the amount of messages sent - includes retrasnmition
        self.incorrect_messages = 0 #stores the amout of messages sent with incorrect md5

        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def mount_package(self, sequence_number, message):
        period = time.time()
        seconds = int(period)
        nanoseconds = int(str(period).split('.')[1])

        message_size = len(bytes(message, 'utf-8'))
        error_code = utils.generate_md5([sequence_number, seconds, nanoseconds, message_size, message])
        pack_format = '!Q Q L H ' + str(message_size) + 's' + str(len(error_code)) + 's'

        packet = struct.pack(pack_format, sequence_number, seconds, nanoseconds, message_size, bytes(message, 'utf-8'), error_code)

        return packet
        # unpacked = struct.unpack(pack_format, packet)
        # print(unpacked[-2].decode("utf-8"))
