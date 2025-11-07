import heapq
from collections import defaultdict, deque
import copy
import json

class Network:
    """Represents a network topology"""
    def __init__(self):
        self.graph = defaultdict(dict)
        self.routers = set()
    
    def add_link(self, router1, router2, cost=1):
        self.graph[router1][router2] = cost
        self.graph[router2][router1] = cost
        self.routers.add(router1)
        self.routers.add(router2)
    
    def get_neighbors(self, router):
        return list(self.graph[router].keys())
    
    def get_cost(self, router1, router2):
        return self.graph[router1].get(router2, float('inf'))

# ==================== PART 1: RIP ====================
class RIPRouter:
    """RIP Router using Bellman-Ford algorithm"""
    def __init__(self, router_id, network):
        self.router_id = router_id
        self.network = network
        self.routing_table = {router_id: (0, router_id)}
        self.updates_received = 0
        self.converged = False
    
    def send_routing_table(self):
        """Returns a copy of routing table for broadcasting"""
        return copy.deepcopy(self.routing_table)
    
    def receive_update(self, neighbor_id, neighbor_table):
        """Receive routing table from neighbor and update local table"""
        updated = False
        cost_to_neighbor = self.network.get_cost(self.router_id, neighbor_id)
        
        for destination, (distance, next_hop) in neighbor_table.items():
            new_distance = distance + cost_to_neighbor
            
            if destination not in self.routing_table:
                self.routing_table[destination] = (new_distance, neighbor_id)
                updated = True
            elif new_distance < self.routing_table[destination][0]:
                self.routing_table[destination] = (new_distance, neighbor_id)
                updated = True
        
        self.updates_received += 1
        return updated

class RIPSimulation:
    """Simulate RIP protocol convergence"""
    def __init__(self, network):
        self.network = network
        self.routers = {r: RIPRouter(r, network) for r in network.routers}
        self.iteration = 0
        self.message_count = 0
    
    def simulate(self, max_iterations=10):
        """Run RIP simulation until convergence"""
        print("=" * 60)
        print("RIP (Routing Information Protocol) Simulation")
        print("=" * 60)
        
        for iteration in range(max_iterations):
            self.iteration = iteration
            updated_any = False
            
            for router_id, router in self.routers.items():
                neighbors = self.network.get_neighbors(router_id)
                routing_table = router.send_routing_table()
                
                for neighbor_id in neighbors:
                    self.routers[neighbor_id].receive_update(router_id, routing_table)
                    self.message_count += 1
                    updated_any = True
            
            print(f"\n--- Iteration {iteration + 1} ---")
            for router_id in sorted(self.routers.keys()):
                print(f"Router {router_id}: {dict(self.routers[router_id].routing_table)}")
            
            if not updated_any:
                print(f"\n✓ Converged after {iteration + 1} iterations")
                print(f"Total messages exchanged: {self.message_count}")
                break
    
    def display_final_tables(self):
        """Display final routing tables"""
        print("\n" + "=" * 60)
        print("Final RIP Routing Tables")
        print("=" * 60)
        for router_id in sorted(self.routers.keys()):
            print(f"\nRouter {router_id}:")
            table = self.routers[router_id].routing_table
            for dest in sorted(table.keys()):
                dist, next_hop = table[dest]
                print(f"  {dest}: Distance={dist}, Next Hop={next_hop}")

# ==================== PART 2: OSPF ====================
class OSPFRouter:
    """OSPF Router using Dijkstra's algorithm"""
    def __init__(self, router_id, network):
        self.router_id = router_id
        self.network = network
        self.link_state_db = {}
        self.routing_table = {}
        self.flood_queue = []
    
    def build_lsa(self):
        """Build Link State Advertisement"""
        lsa = {
            'router': self.router_id,
            'seq_num': 0,
            'links': {}
        }
        for neighbor in self.network.get_neighbors(self.router_id):
            cost = self.network.get_cost(self.router_id, neighbor)
            lsa['links'][neighbor] = cost
        return lsa
    
    def receive_lsa(self, lsa):
        """Receive and flood LSA"""
        router = lsa['router']
        if router not in self.link_state_db or \
           lsa['seq_num'] > self.link_state_db[router].get('seq_num', -1):
            self.link_state_db[router] = lsa
            return True
        return False
    
    def compute_shortest_paths(self):
        """Dijkstra's algorithm to compute SPT"""
        dist = {r: float('inf') for r in self.network.routers}
        dist[self.router_id] = 0
        prev = {r: None for r in self.network.routers}
        visited = set()
        pq = [(0, self.router_id)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            
            if u in self.link_state_db:
                for neighbor, cost in self.link_state_db[u]['links'].items():
                    if neighbor not in visited:
                        new_dist = dist[u] + cost
                        if new_dist < dist[neighbor]:
                            dist[neighbor] = new_dist
                            prev[neighbor] = u
                            heapq.heappush(pq, (new_dist, neighbor))
        
        self.routing_table = {r: (dist[r], prev[r]) for r in self.network.routers}

class OSPFSimulation:
    """Simulate OSPF protocol"""
    def __init__(self, network):
        self.network = network
        self.routers = {r: OSPFRouter(r, network) for r in network.routers}
        self.message_count = 0
    
    def simulate(self):
        """Run OSPF simulation"""
        print("\n" + "=" * 60)
        print("OSPF (Open Shortest Path First) Simulation")
        print("=" * 60)
        
        # Phase 1: Flood LSAs
        print("\n--- Phase 1: LSA Flooding ---")
        all_lsas = {r: self.routers[r].build_lsa() for r in self.network.routers}
        
        for router_id, router in self.routers.items():
            neighbors = self.network.get_neighbors(router_id)
            own_lsa = all_lsas[router_id]
            
            for neighbor_id in neighbors:
                if self.routers[neighbor_id].receive_lsa(own_lsa):
                    self.message_count += 1
        
        # Propagate all LSAs to all routers
        for router in self.routers.values():
            for lsa in all_lsas.values():
                router.receive_lsa(lsa)
        
        # Phase 2: Compute shortest paths
        print("--- Phase 2: Computing Shortest Paths ---")
        for router in self.routers.values():
            router.compute_shortest_paths()
        
        print(f"Total LSA messages: {self.message_count}")
        self.display_final_tables()
    
    def display_final_tables(self):
        """Display final routing tables and SPT"""
        print("\n" + "=" * 60)
        print("Final OSPF Routing Tables (with SPT)")
        print("=" * 60)
        for router_id in sorted(self.routers.keys()):
            print(f"\nRouter {router_id}:")
            table = self.routers[router_id].routing_table
            for dest in sorted(table.keys()):
                dist, next_hop = table[dest]
                if dist != float('inf'):
                    print(f"  {dest}: Distance={dist}, Previous Hop={next_hop}")

# ==================== PART 3: BGP ====================
class BGPRouter:
    """BGP Router with AS path vector"""
    def __init__(self, router_id, as_id, network):
        self.router_id = router_id
        self.as_id = as_id
        self.network = network
        self.routing_table = {}
        self.as_path_db = {}
    
    def advertise_routes(self):
        """Send UPDATE messages to neighbors"""
        updates = {}
        for destination, (path_length, path) in self.as_path_db.items():
            updates[destination] = {
                'as_path': path,
                'path_length': path_length
            }
        return updates
    
    def receive_update(self, neighbor_as, updates):
        """Receive UPDATE from neighbor"""
        updated = False
        for destination, update in updates.items():
            neighbor_path = update['as_path']
            
            # Loop prevention: ignore if local AS in path
            if self.as_id in neighbor_path:
                continue
            
            new_path = neighbor_path + [self.as_id]
            new_length = len(new_path)
            
            if destination not in self.routing_table or \
               new_length < self.routing_table[destination][0]:
                self.routing_table[destination] = (new_length, new_path)
                self.as_path_db[destination] = (new_length, new_path)
                updated = True
        
        return updated

class BGPSimulation:
    """Simulate BGP protocol"""
    def __init__(self, as_topology):
        # as_topology: list of (as_id, neighbors)
        self.routers = {}
        self.as_topology = as_topology
        self.message_count = 0
        
        for as_id, neighbors in as_topology:
            router = BGPRouter(as_id, as_id, None)
            router.routing_table[as_id] = (1, [as_id])
            router.as_path_db[as_id] = (1, [as_id])
            self.routers[as_id] = router
    
    def get_neighbors(self, as_id):
        for aid, neighbors in self.as_topology:
            if aid == as_id:
                return neighbors
        return []
    
    def simulate(self, iterations=10):
        """Run BGP simulation"""
        print("\n" + "=" * 60)
        print("BGP (Border Gateway Protocol) Simulation")
        print("=" * 60)
        
        for iteration in range(iterations):
            updated_any = False
            
            for as_id, router in self.routers.items():
                neighbors = self.get_neighbors(as_id)
                updates = router.advertise_routes()
                
                for neighbor_as in neighbors:
                    if neighbor_as in self.routers:
                        if self.routers[neighbor_as].receive_update(as_id, updates):
                            updated_any = True
                            self.message_count += 1
            
            print(f"\n--- Iteration {iteration + 1} ---")
            for as_id in sorted(self.routers.keys()):
                print(f"AS {as_id}: {self.routers[as_id].routing_table}")
            
            if not updated_any:
                print(f"\n✓ Converged after {iteration + 1} iterations")
                print(f"Total UPDATE messages: {self.message_count}")
                break
        
        self.display_final_tables()
    
    def display_final_tables(self):
        """Display final BGP routing tables"""
        print("\n" + "=" * 60)
        print("Final BGP Routing Tables (AS Paths)")
        print("=" * 60)
        for as_id in sorted(self.routers.keys()):
            print(f"\nAS {as_id}:")
            table = self.routers[as_id].routing_table
            for dest in sorted(table.keys()):
                path_len, path = table[dest]
                print(f"  Destination AS {dest}: AS Path={path}, Length={path_len}")

# ==================== PART 4: IS-IS ====================
class ISISRouter:
    """IS-IS Router using link-state approach"""
    def __init__(self, router_id, network):
        self.router_id = router_id
        self.network = network
        self.lsdb = {}  # Link State Database
        self.routing_table = {}
    
    def build_pdu(self):
        """Build PDU (Protocol Data Unit)"""
        pdu = {
            'router': self.router_id,
            'seq_num': 0,
            'adjacencies': {}
        }
        for neighbor in self.network.get_neighbors(self.router_id):
            metric = self.network.get_cost(self.router_id, neighbor)
            pdu['adjacencies'][neighbor] = metric
        return pdu
    
    def receive_pdu(self, pdu):
        """Receive and process PDU"""
        router = pdu['router']
        if router not in self.lsdb or \
           pdu['seq_num'] > self.lsdb[router].get('seq_num', -1):
            self.lsdb[router] = pdu
            return True
        return False
    
    def compute_spf(self):
        """SPF computation (Dijkstra)"""
        dist = {r: float('inf') for r in self.network.routers}
        dist[self.router_id] = 0
        prev = {r: None for r in self.network.routers}
        visited = set()
        pq = [(0, self.router_id)]
        
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            
            if u in self.lsdb:
                for neighbor, metric in self.lsdb[u]['adjacencies'].items():
                    if neighbor not in visited:
                        new_dist = dist[u] + metric
                        if new_dist < dist[neighbor]:
                            dist[neighbor] = new_dist
                            prev[neighbor] = u
                            heapq.heappush(pq, (new_dist, neighbor))
        
        self.routing_table = {r: (dist[r], prev[r]) for r in self.network.routers}

class ISISSimulation:
    """Simulate IS-IS protocol"""
    def __init__(self, network):
        self.network = network
        self.routers = {r: ISISRouter(r, network) for r in network.routers}
        self.message_count = 0
    
    def simulate(self):
        """Run IS-IS simulation"""
        print("\n" + "=" * 60)
        print("IS-IS (Intermediate System to Intermediate System) Simulation")
        print("=" * 60)
        
        # Phase 1: PDU Flooding
        print("\n--- Phase 1: PDU Flooding ---")
        all_pdus = {r: self.routers[r].build_pdu() for r in self.network.routers}
        
        for router_id, router in self.routers.items():
            neighbors = self.network.get_neighbors(router_id)
            own_pdu = all_pdus[router_id]
            
            for neighbor_id in neighbors:
                if self.routers[neighbor_id].receive_pdu(own_pdu):
                    self.message_count += 1
        
        # Propagate all PDUs
        for router in self.routers.values():
            for pdu in all_pdus.values():
                router.receive_pdu(pdu)
        
        # Phase 2: SPF Computation
        print("--- Phase 2: SPF Computation ---")
        for router in self.routers.values():
            router.compute_spf()
        
        print(f"Total PDU messages: {self.message_count}")
        self.display_final_tables()
    
    def display_final_tables(self):
        """Display final routing tables"""
        print("\n" + "=" * 60)
        print("Final IS-IS Routing Tables")
        print("=" * 60)
        for router_id in sorted(self.routers.keys()):
            print(f"\nRouter {router_id}:")
            table = self.routers[router_id].routing_table
            for dest in sorted(table.keys()):
                dist, prev_hop = table[dest]
                if dist != float('inf'):
                    print(f"  {dest}: Distance={dist}, Previous Hop={prev_hop}")

# ==================== MAIN SIMULATION ====================
if __name__ == "__main__":
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║     ROUTING PROTOCOLS SIMULATION IN PYTHON                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    # Create network topology for RIP, OSPF, IS-IS
    network = Network()
    network.add_link('A', 'B', 1)
    network.add_link('A', 'C', 4)
    network.add_link('B', 'C', 2)
    network.add_link('B', 'D', 5)
    network.add_link('C', 'D', 1)
    network.add_link('D', 'E', 3)
    
    print("\n📡 Network Topology:")
    print("   A -- B -- D -- E")
    print("    \\   |   /")
    print("     \\ | /")
    print("       C")
    
    # Part 1: RIP
    rip_sim = RIPSimulation(network)
    rip_sim.simulate(max_iterations=10)
    rip_sim.display_final_tables()
    
    # Part 2: OSPF
    ospf_sim = OSPFSimulation(network)
    ospf_sim.simulate()
    
    # Part 3: BGP
    as_topology = [
        ('AS1', ['AS2', 'AS3']),
        ('AS2', ['AS1', 'AS4']),
        ('AS3', ['AS1', 'AS4']),
        ('AS4', ['AS2', 'AS3'])
    ]
    bgp_sim = BGPSimulation(as_topology)
    bgp_sim.simulate(iterations=6)
    
    # Part 4: IS-IS
    isis_sim = ISISSimulation(network)
    isis_sim.simulate()
    
    print("\n" + "=" * 60)
    print("✓ All Simulations Completed Successfully!")
    print("=" * 60)