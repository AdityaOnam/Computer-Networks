import matplotlib.pyplot as plt
import random

def tcp_congestion_control(max_rounds, ssthresh_init, loss_probability):
    """
    Simulate TCP Congestion Control with Slow Start, Congestion Avoidance, and Timeout
    
    Args:
        max_rounds: Maximum transmission rounds
        ssthresh_init: Initial slow start threshold
        loss_probability: Probability of packet loss (0 to 1)
    """
    cwnd = 1  # Congestion window (in MSS)
    ssthresh = ssthresh_init  # Slow start threshold
    
    cwnd_history = []
    round_history = []
    phase_history = []
    
    print("=" * 60)
    print("TCP Congestion Control Simulation")
    print("=" * 60)
    print(f"Initial cwnd: {cwnd}")
    print(f"Initial ssthresh: {ssthresh}")
    print(f"Loss Probability: {loss_probability}\n")
    
    for round_num in range(max_rounds):
        cwnd_history.append(cwnd)
        round_history.append(round_num)
        
        # Determine current phase
        if cwnd < ssthresh:
            phase = "Slow Start"
            phase_history.append(1)
        else:
            phase = "Congestion Avoidance"
            phase_history.append(2)
        
        print(f"Round {round_num}: cwnd = {cwnd:.2f}, ssthresh = {ssthresh}, Phase = {phase}")
        
        # Simulate packet loss
        packet_lost = random.random() < loss_probability
        
        if packet_lost:
            print(f"  -> Packet loss detected! Timeout occurred.")
            # Multiplicative decrease
            ssthresh = max(cwnd / 2, 2)
            cwnd = 1  # Reset to 1 on timeout
            print(f"  -> ssthresh updated to {ssthresh}, cwnd reset to 1\n")
            phase_history[-1] = 3  # Mark as timeout phase
        else:
            # Successful ACK received
            if cwnd < ssthresh:
                # Slow Start: exponential growth
                cwnd = cwnd * 2
                print(f"  -> ACK received. cwnd doubled to {cwnd}\n")
            else:
                # Congestion Avoidance: linear growth
                cwnd = cwnd + 1
                print(f"  -> ACK received. cwnd increased by 1 to {cwnd}\n")
    
    # Plot the results
    plt.figure(figsize=(12, 7))
    
    # Main plot: cwnd over time
    plt.subplot(2, 1, 1)
    colors = []
    for i, phase in enumerate(phase_history):
        if phase == 1:
            colors.append('green')
        elif phase == 2:
            colors.append('blue')
        else:
            colors.append('red')
    
    plt.plot(round_history, cwnd_history, marker='o', linestyle='-', linewidth=2, markersize=6)
    for i in range(len(round_history)):
        plt.plot(round_history[i], cwnd_history[i], 'o', color=colors[i], markersize=8)
    
    plt.xlabel('Transmission Round', fontsize=12, fontweight='bold')
    plt.ylabel('Congestion Window (cwnd)', fontsize=12, fontweight='bold')
    plt.title('TCP Congestion Control: cwnd vs Transmission Rounds', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(['cwnd'], loc='upper left')
    
    # Add phase annotations
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Slow Start'),
        Patch(facecolor='blue', label='Congestion Avoidance'),
        Patch(facecolor='red', label='Timeout/Loss')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    # Secondary plot: phase visualization
    plt.subplot(2, 1, 2)
    plt.scatter(round_history, phase_history, c=colors, s=100, alpha=0.6)
    plt.xlabel('Transmission Round', fontsize=12, fontweight='bold')
    plt.ylabel('Phase', fontsize=12, fontweight='bold')
    plt.yticks([1, 2, 3], ['Slow Start', 'Congestion\nAvoidance', 'Timeout'])
    plt.title('TCP Phase Transitions', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('cwnd_plot.png', dpi=300, bbox_inches='tight')
    print("=" * 60)
    print("Plot saved as 'cwnd_plot.png'")
    print("=" * 60)
    plt.show()

if __name__ == "__main__":
    # Configure simulation parameters
    MAX_ROUNDS = 25
    SSTHRESH_INIT = 16
    LOSS_PROBABILITY = 0.15  # 15% chance of packet loss
    
    random.seed(42)  # For reproducible results
    tcp_congestion_control(MAX_ROUNDS, SSTHRESH_INIT, LOSS_PROBABILITY)