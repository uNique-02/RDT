import Receiver
import Packet
import time

class Sender:
    timeout = 2
    receiver = Receiver.Receiver()
    seq = 1
    
    def __init__(self):
        print("[Sender] Initialized")
        self.packets = self.generate_packets()
        self.send(self.packets)

    def generate_packets(self):
        packets = []
        for i in range(0, 10):
            
            packets.append(Packet.Packet(self.toggle(self.seq), f"Message {i}"))
        return packets

    def send(self, packets):
        for packet in packets:
            self.send_packet(packet)
            # self.start_timer()
            while True:
                ack = self.receiver.acknowledge(packet)
                if ack is not None:
                    # self.stop_timer()
                    break
                else:
                    self.send_packet(packet)
                    self.start_timer()

    def toggle(self, seq_num):
        self.seq = 1 if seq_num == 0 else 0
        return self.seq
    
    def send_packet(self, packet):
        if packet.loss_prob > 60:
            print(f"[Network] Packet Lost: Packet({packet.seq_num}, data={packet.data})")
            self.start_countdown()
            packet.loss_prob = packet.generate_probability()
            packet.corrupt_prob = packet.generate_probability()
            self.send_packet(packet)
        else:
            print(f"[Sender][Stop and Wait][Sending] Packet({packet.seq_num}, data={packet.data})")
            ack = self.receiver.acknowledge(packet)
            if ack == "NACK":
                print(f"[Network] Packet Corrupted: Packet({packet.seq_num}, data={packet.data})")
                self.start_countdown()
                packet.loss_prob = packet.generate_probability()
                packet.corrupt_prob = packet.generate_probability()
                self.send_packet(packet)
            else:
                self.toggle(packet)
    
    def start_timer(self):
        self.start_time = time.time()
    
    def stop_timer(self):
        self.end_time = time.time()
        print(f"Packet acknowledged in {(self.end_time - self.start_time):.3f} seconds")
    
    def start_countdown(self, seconds_countdown=2):
        print("[Sender] Resending packet")
        while seconds_countdown > 0:
            time.sleep(1)
            seconds_countdown -= 1

    def stop(self):
        self.end_time = time.time()
        print(f"\n\nTotal elapsed time: {(self.end_time - self.start_time):.3f} seconds\n")
        exit(0)

if __name__ == "__main__":
    sender = Sender()
