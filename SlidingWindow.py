import collections
from threading import Timer

class SlidingWindowElement:
    def __init__(self, packet, sequence_number, timeout, handler):
        self.packet = packet
        self.ack = False
        self.timer = Timer(timeout, handler)
        self.sequence_number = sequence_number

class SlidingWindow:
    def __init__(self, window_size):
        self.window_size = window_size
        self.current_size = 0
        self.buffer = collections.deque(maxlen=window_size)

    def insert(self, element):
        self.buffer.append(element)
        if (self.current_size < self.window_size):
            self.current_size += 1