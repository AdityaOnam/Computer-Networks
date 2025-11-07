# ip_utils.py
from typing import Tuple

def ip_to_binary(ip_address: str) -> str:
    """
    Convert dotted-decimal IPv4 address to 32-bit binary string.
    Example: "192.168.1.1" -> "11000000101010000000000100000001"
    """
    octets = ip_address.strip().split(".")
    if len(octets) != 4:
        raise ValueError(f"Invalid IPv4 address: {ip_address}")
    bits = []
    for o in octets:
        n = int(o)
        if n < 0 or n > 255:
            raise ValueError(f"Invalid octet in IP: {o}")
        bits.append(f"{n:08b}")
    return "".join(bits)

def get_network_prefix(ip_cidr: str) -> str:
    """
    Given a CIDR string like "200.23.16.0/23",
    return the network prefix bits as a string (length = mask length).
    Example -> "11001000000101110001000" (23 bits)
    """
    ip_part, prefix_len_str = ip_cidr.strip().split("/")
    prefix_len = int(prefix_len_str)
    if prefix_len < 0 or prefix_len > 32:
        raise ValueError(f"Invalid prefix length: {prefix_len}")
    ip_bits = ip_to_binary(ip_part)
    return ip_bits[:prefix_len]

if __name__ == "__main__":
    # Quick manual test
    print("ip_to_binary('192.168.1.1') =", ip_to_binary("192.168.1.1"))
    print("get_network_prefix('200.23.16.0/23') =", get_network_prefix("200.23.16.0/23"))