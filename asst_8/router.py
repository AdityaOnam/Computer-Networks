# router.py
from typing import List, Tuple
from ip_utils import ip_to_binary, get_network_prefix

class Router:
    def __init__(self, routes: List[Tuple[str, str]]):
        """
        routes: list of tuples (cidr_prefix_string, output_link_string)
        Example: [("223.1.1.0/24", "Link 0"), ...]
        """
        self._forwarding_table = []
        self.build_forwarding_table(routes)

    def build_forwarding_table(self, routes: List[Tuple[str, str]]):
        """
        Convert human-readable routes into internal table of:
        (prefix_bits, prefix_length, output_link)
        and sort by prefix_length descending to simplify LPM.
        """
        tbl = []
        for cidr, link in routes:
            prefix_bits = get_network_prefix(cidr)
            tbl.append((prefix_bits, len(prefix_bits), link))
        # Sort by prefix length (longest first)
        tbl.sort(key=lambda t: t[1], reverse=True)
        self._forwarding_table = tbl

    def route_packet(self, dest_ip: str) -> str:
        """
        Longest Prefix Match: return output link string or "Default Gateway".
        """
        dest_bits = ip_to_binary(dest_ip)
        for prefix_bits, plen, link in self._forwarding_table:
            if dest_bits.startswith(prefix_bits):
                return link
        return "Default Gateway"

if __name__ == "__main__":
    # Test case from assignment
    routes = [
        ("223.1.1.0/24", "Link 0"),
        ("223.1.2.0/24", "Link 1"),
        ("223.1.3.0/24", "Link 2"),
        ("223.1.0.0/16", "Link 4 (ISP)")
    ]
    r = Router(routes)
    tests = [
        ("223.1.1.100", "Link 0"),
        ("223.1.2.5", "Link 1"),
        ("223.1.250.1", "Link 4 (ISP)"),
        ("198.51.100.1", "Default Gateway")
    ]
    for ip, expected in tests:
        out = r.route_packet(ip)
        print(f"{ip} -> {out}  (expected: {expected})")