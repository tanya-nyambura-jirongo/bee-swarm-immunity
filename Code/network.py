# network.py - Network topology and message routing

import numpy as np
from typing import List, Dict

class Network:
    """Network topology for agent communication."""
    
    def __init__(self, num_agents: int, topology: str = 'mesh'):
        self.num_agents = num_agents
        self.topology = topology
        self.adjacency = self._create_topology()
    
    def _create_topology(self) -> np.ndarray:
        """Create network topology adjacency matrix."""
        if self.topology == 'mesh':
            adj = np.ones((self.num_agents, self.num_agents))
            np.fill_diagonal(adj, 0)
        
        elif self.topology == 'star':
            adj = np.zeros((self.num_agents, self.num_agents))
            adj[0, 1:] = 1
            adj[1:, 0] = 1
        
        elif self.topology == 'ring':
            adj = np.zeros((self.num_agents, self.num_agents))
            for i in range(self.num_agents):
                adj[i, (i + 1) % self.num_agents] = 1
                adj[(i + 1) % self.num_agents, i] = 1
        
        else:
            raise ValueError(f"Unknown topology: {self.topology}")
        
        return adj
    
    def neighbors(self, agent_id: int) -> List[int]:
        """Get neighbors of an agent."""
        return [i for i in range(self.num_agents) if self.adjacency[agent_id, i] == 1]
    
    def route_message(self, message: Dict) -> None:
        """Route a message through the network."""
        pass
    
    def get_peer_history(self, agent_id: int) -> List[Dict]:
        """Get historical data about a peer."""
        return []
