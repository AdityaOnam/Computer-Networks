# scheduler.py
from dataclasses import dataclass
from typing import List
import copy

@dataclass
class Packet:
    source_ip: str
    dest_ip: str
    payload: str
    priority: int  # 0=High, 1=Medium, 2=Low

def fifo_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    First-Come, First-Served: return packets in arrival order.
    Return a new list (shallow copies of packet objects).
    """
    return list(packet_list)  # returns a new list preserving order

def priority_scheduler(packet_list: List[Packet]) -> List[Packet]:
    """
    Priority scheduler: lower priority value means higher priority.
    Preserve arrival order among same-priority packets.
    """
    # To ensure stable ordering among equal priority, attach arrival index
    indexed = list(enumerate(packet_list))
    # Sort by (priority, arrival_index)
    indexed.sort(key=lambda iv: (iv[1].priority, iv[0]))
    return [pkt for idx, pkt in indexed]

if __name__ == "__main__":
    # Build test packets in arrival order
    packets = [
        Packet("10.0.0.1", "10.0.0.2", "Data Packet 1", priority=2),
        Packet("10.0.0.3", "10.0.0.4", "Data Packet 2", priority=2),
        Packet("10.0.0.5", "10.0.0.6", "VOIP Packet 1", priority=0),
        Packet("10.0.0.7", "10.0.0.8", "Video Packet 1", priority=1),
        Packet("10.0.0.9", "10.0.0.10", "VOIP Packet 2", priority=0),
    ]

    fifo_out = fifo_scheduler(packets)
    priority_out = priority_scheduler(packets)

    print("FIFO payload order:", [p.payload for p in fifo_out])
    print("Expected FIFO: ['Data Packet 1', 'Data Packet 2', 'VOIP Packet 1', 'Video Packet 1', 'VOIP Packet 2']")
    print("Priority payload order:", [p.payload for p in priority_out])
    print("Expected Priority: ['VOIP Packet 1', 'VOIP Packet 2', 'Video Packet 1', 'Data Packet 1', 'Data Packet 2']")
