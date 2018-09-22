import collections
from threading import Timer
from copy import deepcopy

class SlidingWindowElement:
    def __init__(self, packet, sequence_number, timeout, handler):
        self.packet = deepcopy(packet)
        self.ack = False
        self.sequence_number = sequence_number
        self.timer = Timer(timeout, handler, [self])
    
    def set_ack(self):
        self.ack = True
        self.timer.cancel()

    def reset_timer(self, timeout, handler):
        timer = Timer(timeout, handler, [self])
        self.timer.cancel()
        self.timer = timer
        self.timer.start()

class SlidingWindow:
    def __init__(self, window_size):
        self.window_size = window_size
        self.current_size = 0
        self.buffer = collections.deque(maxlen=window_size)

    def insert(self, element):
        self.buffer.append(element)
        if (self.current_size < self.window_size):
            self.current_size += 1

    def find_in_list(self, sequence_number):
        for element in self.buffer:
            if(element.sequence_number == sequence_number):
                return element
        
        return None

    def print_list(self):
        for element in self.buffer:
            print(element.sequence_number, element.ack)
    
    def check_all_acks(self):
        for element in self.buffer:
            if(element.ack == False):
                return False
            
        return True