import random

class Receiver:
    def __init__(self):
        self._state = None

    def acknowledge(self, packet):
        if packet.corrupt_prob < 60:
            return "NACK"
        return "ACK"
