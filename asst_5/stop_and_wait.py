import random
import time

def stop_and_wait_arq(total_frames=5, loss_probability=0.3, timeout=2):
    """
    Simulate Stop-and-Wait ARQ protocol
    
    Parameters:
    - total_frames: Total number of frames to send
    - loss_probability: Probability of frame/ACK loss (0-1)
    - timeout: Timeout duration in seconds
    """
    print("=" * 50)
    print("Stop-and-Wait ARQ Simulation")
    print("=" * 50)
    print(f"Total Frames: {total_frames}")
    print(f"Loss Probability: {loss_probability}")
    print(f"Timeout: {timeout}s\n")
    
    frame_number = 0
    total_transmissions = 0
    retransmissions = 0
    
    while frame_number < total_frames:
        print(f"Sending Frame {frame_number}")
        total_transmissions += 1
        
        # Simulate frame transmission with possible loss
        frame_lost = random.random() < loss_probability
        
        if frame_lost:
            print(f"Frame {frame_number} lost, retransmitting...")
            retransmissions += 1
            time.sleep(0.5)  # Simulate timeout
            continue
        
        # Simulate ACK transmission with possible loss
        ack_lost = random.random() < loss_probability
        
        if ack_lost:
            print(f"ACK {frame_number} lost, retransmitting...")
            retransmissions += 1
            time.sleep(0.5)  # Simulate timeout
            continue
        
        # Successful transmission
        print(f"ACK {frame_number} received")
        print()
        frame_number += 1
    
    print("=" * 50)
    print("Transmission Complete!")
    print(f"Total Frames Sent: {total_frames}")
    print(f"Total Transmissions: {total_transmissions}")
    print(f"Retransmissions: {retransmissions}")
    print(f"Efficiency: {(total_frames/total_transmissions)*100:.2f}%")
    print("=" * 50)

if __name__ == "__main__":
    # Run simulation with default parameters
    stop_and_wait_arq(total_frames=5, loss_probability=0.3, timeout=2)
    
    print("\n\n")
    
    # Run with different parameters
    print("Running with higher loss probability:")
    stop_and_wait_arq(total_frames=5, loss_probability=0.5, timeout=2)