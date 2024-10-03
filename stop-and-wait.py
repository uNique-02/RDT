timeout = 5

def stop_and_wait():
    while True:
        # Send the packet
        send_packet()
        # Start the timer
        start_timer()
        while True:
            # Wait for the ACK
            ack = wait_for_ack(timeout)
            if ack is not None:
                # Stop the timer
                stop_timer()
                break
            else:
                # Resend the packet
                send_packet()
                # Restart the timer
                start_timer()
                
def send_packet():
    pass

def start_timer():
    pass

def wait_for_ack(timeout):
    pass

def stop_timer():
    pass
