import collections

class SlidingWindowElement:
    def __init__(self, sequence_number, message=None):
        self.sequence_number = sequence_number
        self.message = message

class ServerSlidingWindow:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buffer = collections.deque(maxlen=window_size)
        self.current_size = 0

        for i in range(0, self.window_size):
            element = SlidingWindowElement(i)
            self.buffer.append(element)
    
    def slide_window(self, quantity):
        for _ in range(0, quantity):
            next_sequence_number = self.buffer[-1].sequence_number + 1
            next_element = SlidingWindowElement(next_sequence_number)

            self.buffer.append(next_element)

    
