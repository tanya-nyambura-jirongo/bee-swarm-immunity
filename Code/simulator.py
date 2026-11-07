# simulator.py - Main simulation engine

import numpy as np
import random
from typing import List, Dict
from agent import Agent
from network import Network
from task import TaskQueue

class Simulator:
    """Discrete-event simulator for bee-inspired agent swarms."""
    
    def __init__(self, num_agents: int = 20, topology: str = 'mesh', 
                 num_timesteps: int = 100):
        self.num_agents = num_agents
        self.topology = topology
        self.num_timesteps = num_timesteps
        
        self.agents = [Agent(i) for i in range(num_agents)]
        self.network = Network(num_agents, topology)
        self.task_queue = TaskQueue()
        
        self.compromised_agents = set()
        self.isolated_agents = set()
        self.isolation_events = []
        self.monitor = Monitor()
    
    def introduce_compromised_agent(self, agent_id: int) -> None:
        """Introduce a compromised agent into the swarm."""
        self.agents[agent_id].state = 'compromised'
        self.compromised_agents.add(agent_id)
    
    def step(self, timestep: int) -> None:
        """Execute one simulation step."""
        for agent in self.agents:
            if agent.state != 'dead':
                agent.update_state(timestep)
        
        self._peer_detection_phase(timestep)
        self._environmental_disruption_phase(timestep)
        self._contagion_phase(timestep)
        
        for agent in self.agents:
            if agent.state not in ['dead', 'isolated']:
                agent.execute_tasks(self.task_queue)
        
        self._record_monitoring_data(timestep)
    
    def _peer_detection_phase(self, timestep: int) -> None:
        """Layer 2: Peer detection and collective isolation."""
        isolation_candidates = {}
        
        for agent in self.agents:
            if agent.state in ['dead', 'isolated']:
                continue
            
            for peer_id in self.network.neighbors(agent.id):
                peer = self.agents[peer_id]
                
                if peer.state == 'compromised':
                    if peer_id not in isolation_candidates:
                        isolation_candidates[peer_id] = 0
                    isolation_candidates[peer_id] += 1
        
        for peer_id, votes in isolation_candidates.items():
            neighbors = len(list(self.network.neighbors(peer_id)))
            if neighbors > 0 and votes / neighbors > 0.6:
                self.agents[peer_id].state = 'isolated'
                self.isolated_agents.add(peer_id)
                self.isolation_events.append({
                    'timestep': timestep,
                    'agent_id': peer_id
                })
    
    def _environmental_disruption_phase(self, timestep: int) -> None:
        """Layer 3: Environmental disruption and adaptation."""
        compromised_ratio = len(self.compromised_agents) / self.num_agents
        
        if compromised_ratio > 0.2:
            for agent_id in list(self.isolated_agents):
                if random.random() < 0.1:
                    self.agents[agent_id].state = 'dead'
                    self.isolated_agents.discard(agent_id)
    
    def _contagion_phase(self, timestep: int) -> None:
        """Spread compromise from compromised agents to healthy agents."""
        newly_compromised = []
        
        for agent in self.agents:
            if agent.state == 'compromised':
                for neighbor_id in self.network.neighbors(agent.id):
                    neighbor = self.agents[neighbor_id]
                    if neighbor.state == 'healthy' and random.random() < 0.15:
                        newly_compromised.append(neighbor_id)
        
        for agent_id in newly_compromised:
            self.agents[agent_id].state = 'suspicious'
            self.compromised_agents.add(agent_id)
    
    def _record_monitoring_data(self, timestep: int) -> None:
        """Record swarm health metrics."""
        compromised_count = len(self.compromised_agents)
        isolated_count = len(self.isolated_agents)
        
        coherence_scores = [a.coherence_history[-1] if a.coherence_history else 0.5 
                           for a in self.agents if a.state != 'dead']
        health_score = np.mean(coherence_scores) if coherence_scores else 0.0
        
        self.monitor.record({
            'timestep': timestep,
            'compromised': compromised_count,
            'isolated': isolated_count,
            'health': health_score
        })
    
    def run(self, verbose: bool = True) -> None:
        """Run complete simulation."""
        for t in range(self.num_timesteps):
            self.step(t)
            
            if verbose and t % 20 == 0:
                print(f"  Timestep {t}: "
                      f"Compromised={len(self.compromised_agents)}, "
                      f"Isolated={len(self.isolated_agents)}")


class Monitor:
    """Monitor swarm health and metrics."""
    
    def __init__(self):
        self.data = []
        self.contagion_history = []
    
    def record(self, metrics: Dict) -> None:
        """Record metrics for a timestep."""
        self.data.append(metrics)
        self.contagion_history.append({
            'timestep': metrics['timestep'],
            'newly_compromised': metrics['compromised']
        })
