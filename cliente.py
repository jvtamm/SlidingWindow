import struct, binascii, time, socket
import utils
from sys import argv
from Transmitter import Transmitter
from ClientSlidingWindow import SlidingWindowElement

def main(argv):
    start_time = time.time()
    ip, port = argv[2].split(':')
    transmitter = Transmitter(int(argv[3]), float(argv[5]), int(argv[4]), ip, int(port))

    # transmitter.udp.bind((socket.gethostname(), 3000))

    with open(argv[1]) as fp:
        sequence_number = 1
        for line in fp: 
            # packet = transmitter.mount_packet(sequence_number, line.split('\n')[0])
            packet = transmitter.mount_packet(sequence_number, line)

            window_element = SlidingWindowElement(packet, sequence_number, transmitter.timeout, transmitter.resend_packet)
            transmitter.window.insert(window_element)  # insere na janela
    
            if (utils.compare_error(transmitter.p_error)):
                packet = utils.corrupt_md5(packet)
                transmitter.incorrect_messages += 1

            transmitter.send_packet(packet)
            window_element.timer.start()    # seta timeout
            sequence_number += 1

            if (transmitter.window.current_size == transmitter.window.window_size):
                while(not transmitter.window.buffer[0].ack):
                    transmitter.handle_ack()

            # transmitter.window.print_list()
            # print()
            # se tamanho atual da janela = tamanho maximo espere a primeira mensagem receber o ack
            # checa md5 e desliza a janela
            # lembrar de setar ack para mensagens recebidas fora de ordem
    
    while(not transmitter.window.check_all_acks()):
        transmitter.handle_ack()

    print(
        transmitter.messages, 
        transmitter.messages_sent, 
        transmitter.incorrect_messages, 
        round(time.time() - start_time, 3)
        )


if __name__ == '__main__':
    main(argv)