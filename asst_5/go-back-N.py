import random
import time

def go_back_n_arq(total_frames, window_size, loss_probability):
    """
    Simulate Go-Back-N ARQ protocol
    
    Args:
        total_frames: Total number of frames to transmit
        window_size: Size of the sliding window
        loss_probability: Probability of frame loss (0 to 1)
    """
    print("=" * 60)
    print("Go-Back-N ARQ Simulation")
    print("=" * 60)
    print(f"Total Frames: {total_frames}")
    print(f"Window Size: {window_size}")
    print(f"Loss Probability: {loss_probability}\n")
    
    base = 0  # Base of the window
    next_seq = 0  # Next sequence number to send
    frames_sent = 0
    frames_retransmitted = 0
    
    while base < total_frames:
        # Send frames within the window
        while next_seq < base + window_size and next_seq < total_frames:
            if next_seq == base:
                window_end = min(base + window_size - 1, total_frames - 1)
                print(f"Sending frames {base}-{window_end}")
            next_seq += 1
            frames_sent += 1
        
        time.sleep(0.3)
        
        # Simulate receiving ACKs
        ack_received = base
        frame_lost = False
        
        # Check each frame in the window for loss
        for i in range(base, next_seq):
            if random.random() < loss_probability:
                print(f"Frame {i} lost, retransmitting frames {i}-{next_seq - 1}")
                frame_lost = True
                frames_retransmitted += (next_seq - i)
                next_seq = i  # Go back to the lost frame
                break
            else:
                ack_received = i
        
        if not frame_lost:
            # All frames acknowledged successfully
            print(f"ACK {ack_received} received")
            base = ack_received + 1
            
            if base < total_frames:
                window_end = min(base + window_size - 1, total_frames - 1)
                print(f"Window slides to {base}-{window_end}")
            print()
        else:
            time.sleep(0.3)
    
    print("=" * 60)
    print("Transmission Complete!")
    print(f"Total frames sent (including retransmissions): {frames_sent}")
    print(f"Frames retransmitted: {frames_retransmitted}")
    print(f"Efficiency: {(total_frames / frames_sent) * 100:.2f}%")
    print("=" * 60)

if __name__ == "__main__":
    # Configure simulation parameters
    TOTAL_FRAMES = 10
    WINDOW_SIZE = 4
    LOSS_PROBABILITY = 0.2  # 20% chance of loss
    
    random.seed(42)  # For reproducible results
    go_back_n_arq(TOTAL_FRAMES, WINDOW_SIZE, LOSS_PROBABILITY)