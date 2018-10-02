from threading import Timer
from ServerSlidingWindow import ServerSlidingWindow

class Client:
    def __init__(self, window_size, address):
        self.address = address
        self.window = ServerSlidingWindow(window_size)
        # self.timer = Timer(60.0, handler, [self.address])

    
    def save_message(self, message, sequence_number):
        for element in self.window.buffer:
            if(element.sequence_number == sequence_number):
                element.message = message

    def print_window(self):
        for element in self.window.buffer:
            print(element.sequence_number, element.message)
    
