import struct
import utils
from sys import argv
from Transmitter import Transmitter
from SlidingWindow import SlidingWindowElement

if __name__ == '__main__':
    transmitter = Transmitter(int(argv[3]))

    """Connect to socket"""
    ip, port = argv[2].split(':')
    transmitter.udp.connect((ip, int(port)))

    with open(argv[1]) as fp:
        sequence_number = 0
        for line in fp:
            error = utils.compare_error(float(argv[5]))
            packet = transmitter.mount_packet(sequence_number, line.split('\n')[0], error)

            window_element = SlidingWindowElement(sequence_number, packet, int(argv[4]), transmitter.hello)
            transmitter.window.insert(window_element)  # insere na janela

            transmitter.udp.send(packet)    # envia pacote
            window_element.timer.start()    # seta timeout
            sequence_number += 1

            # if (transmitter.window.current_size == transmitter.window.window_size):
            #     while(not transmitter.window.buffer[0].ack):
            #         recv
            #         print('awaiting for first ack')
            # se tamanho atual da janela = tamanho maximo espere a primeira mensagem receber o ack
            # checa md5 e desliza a janela
            # lembrar de setar ack para mensagens recebidas fora de ordem