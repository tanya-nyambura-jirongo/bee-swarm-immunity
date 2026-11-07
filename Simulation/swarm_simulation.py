"""
Bee-Inspired Peer Immunity Defense System for AI Agent Swarms
Simulates multi-agent swarms with peer-based detection and isolation
"""

import json
import csv
import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple
from enum import Enum
from datetime import datetime
import math

# ============================================================================
# ENUMS AND DATA CLASSES
# ============================================================================

class AgentState(Enum):
    HEALTHY = "healthy"
    COMPROMISED = "compromised"
    ISOLATED = "isolated"
    REMOVED = "removed"

class NetworkTopology(Enum):
    MESH = "mesh"
    STAR = "star"
    RING = "ring"

@dataclass
class AgentProperties:
    """Five measurable agent properties (0.0 - 1.0)"""
    coherence: float  # Output consistency
    fidelity: float  # Message relay accuracy
    refusal_robustness: float  # Task refusal consistency
    detection_sensitivity: float  # Anomaly detection accuracy
    compliance: float  # Adherence to isolation directives

    def swarm_health_score(self) -> float:
        """Calculate swarm health score: 0.2 × sum of all properties"""
        avg = (self.coherence + self.fidelity + self.refusal_robustness + 
               self.detection_sensitivity + self.compliance) / 5.0
        return avg

@dataclass
class Agent:
    """Individual agent in the swarm"""
    id: int
    state: AgentState
    properties: AgentProperties
    neighbors: List[int]
    tasks_completed: int = 0
    harmful_tasks_refused: int = 0
    decomposed_tasks_completed: int = 0
    detection_votes: int = 0
    isolation_votes: int = 0
    
    def is_healthy(self) -> bool:
        return self.state == AgentState.HEALTHY
    
    def is_compromised(self) -> bool:
        return self.state == AgentState.COMPROMISED

@dataclass
class SimulationStep:
    """Record of a single simulation timestep"""
    timestep: int
    total_agents: int
    healthy_agents: int
    compromised_agents: int
    isolated_agents: int
    removed_agents: int
    avg_coherence: float
    avg_fidelity: float
    avg_refusal: float
    avg_detection: float
    avg_compliance: float
    swarm_health_score: float
    total_tasks_completed: int
    harmful_tasks_refused: int
    decomposed_tasks_completed: int
    containment_ratio: float
    cooperation_rate: float
    contagion_spread: int

# ============================================================================
# SWARM SIMULATION CLASS
# ============================================================================

class SwarmSimulation:
    def __init__(
        self,
        num_agents: int,
        topology: NetworkTopology,
        num_compromised: int = 1,
        timesteps: int = 50,
        seed: int = None
    ):
        self.num_agents = num_agents
        self.topology = topology
        self.num_compromised = num_compromised
        self.timesteps = timesteps
        self.agents: Dict[int, Agent] = {}
        self.logs: List[SimulationStep] = []
        self.task_queue: List[Dict] = []
        
        if seed:
            random.seed(seed)
        
        self._initialize_agents()
        self._initialize_network()
        self._initialize_compromised_agents()
        self._generate_tasks()
    
    def _initialize_agents(self):
        """Create all agents with random properties"""
        for i in range(self.num_agents):
            properties = AgentProperties(
                coherence=random.uniform(0.7, 1.0),
                fidelity=random.uniform(0.7, 1.0),
                refusal_robustness=random.uniform(0.7, 1.0),
                detection_sensitivity=random.uniform(0.6, 0.95),
                compliance=random.uniform(0.7, 1.0)
            )
            self.agents[i] = Agent(
                id=i,
                state=AgentState.HEALTHY,
                properties=properties,
                neighbors=[]
            )
    
    def _initialize_network(self):
        """Create network topology and connect agents"""
        if self.topology == NetworkTopology.MESH:
            self._create_mesh()
        elif self.topology == NetworkTopology.STAR:
            self._create_star()
        elif self.topology == NetworkTopology.RING:
            self._create_ring()
    
    def _create_mesh(self):
        """Fully connected mesh network"""
        for i in range(self.num_agents):
            self.agents[i].neighbors = [j for j in range(self.num_agents) if j != i]
    
    def _create_star(self):
        """Star topology: agent 0 is hub, all others connect to hub"""
        hub_id = 0
        for i in range(self.num_agents):
            if i == hub_id:
                self.agents[i].neighbors = [j for j in range(self.num_agents) if j != i]
            else:
                self.agents[i].neighbors = [hub_id]
    
    def _create_ring(self):
        """Ring topology: each agent connects to two neighbors"""
        for i in range(self.num_agents):
            prev_neighbor = (i - 1) % self.num_agents
            next_neighbor = (i + 1) % self.num_agents
            self.agents[i].neighbors = [prev_neighbor, next_neighbor]
    
    def _initialize_compromised_agents(self):
        """Mark random agents as compromised"""
        compromised_ids = random.sample(range(self.num_agents), self.num_compromised)
        for agent_id in compromised_ids:
            self.agents[agent_id].state = AgentState.COMPROMISED
            # Compromised agents have degraded properties
            self.agents[agent_id].properties.coherence = random.uniform(0.2, 0.5)
            self.agents[agent_id].properties.fidelity = random.uniform(0.2, 0.5)
            self.agents[agent_id].properties.refusal_robustness = random.uniform(0.1, 0.4)
    
    def _generate_tasks(self):
        """Generate task queue with whole and decomposed tasks"""
        for _ in range(self.timesteps * 2):
            # Whole task (high refusal rate)
            self.task_queue.append({
                "type": "whole",
                "harmful": random.random() < 0.3,
                "refusal_rate": 0.895 if random.random() < 0.5 else 0.1
            })
            # Decomposed task (low refusal rate)
            self.task_queue.append({
                "type": "decomposed",
                "harmful": random.random() < 0.3,
                "refusal_rate": 0.427 if random.random() < 0.5 else 0.1
            })
    
    def run(self) -> List[SimulationStep]:
        """Run the full simulation"""
        print(f"\n{'='*80}")
        print(f"SWARM SIMULATION: {self.num_agents} agents, {self.topology.value} topology")
        print(f"{'='*80}\n")
        
        for timestep in range(self.timesteps):
            # Step 1: Agents execute tasks
            self._execute_tasks(timestep)
            
            # Step 2: Peer detection (Layer 2)
            self._peer_detection(timestep)
            
            # Step 3: Isolation and removal
            self._isolation_and_removal(timestep)
            
            # Step 4: Environmental disruption (Layer 3)
            self._environmental_disruption(timestep)
            
            # Step 5: Log state
            self._log_state(timestep)
            
            # Print progress
            if (timestep + 1) % 10 == 0:
                print(f"Timestep {timestep + 1}/{self.timesteps} complete")
        
        print(f"\n{'='*80}")
        print("SIMULATION COMPLETE")
        print(f"{'='*80}\n")
        
        return self.logs
    
    def _execute_tasks(self, timestep: int):
        """Agents execute tasks from queue"""
        if timestep >= len(self.task_queue):
            return
        
        task = self.task_queue[timestep]
        
        for agent_id, agent in self.agents.items():
            if agent.state == AgentState.REMOVED:
                continue
            
            # Compromised agents are more likely to complete harmful tasks
            if agent.is_compromised():
                completion_rate = 0.8 if task["harmful"] else 0.9
            else:
                completion_rate = (1.0 - agent.properties.refusal_robustness) if task["harmful"] else 0.95
            
            if random.random() < completion_rate:
                agent.tasks_completed += 1
                if task["harmful"]:
                    if task["type"] == "whole":
                        agent.harmful_tasks_refused += 1
                    else:
                        agent.decomposed_tasks_completed += 1
    
    def _peer_detection(self, timestep: int):
        """Layer 2: Peer-based detection and voting"""
        for agent_id, agent in self.agents.items():
            if agent.state == AgentState.REMOVED or agent.state == AgentState.ISOLATED:
                continue
            
            # Agent checks its neighbors
            for neighbor_id in agent.neighbors:
                neighbor = self.agents[neighbor_id]
                if neighbor.state == AgentState.REMOVED:
                    continue
                
                # Calculate anomaly score for neighbor
                anomaly_score = self._calculate_anomaly_score(neighbor)
                
                # If anomaly detected, vote to isolate
                if anomaly_score > 0.5:
                    neighbor.detection_votes += 1
    
    def _calculate_anomaly_score(self, agent: Agent) -> float:
        """Calculate how anomalous an agent is (0.0 - 1.0)"""
        if agent.is_healthy():
            return 0.0
        
        # Compromised agents have low coherence and fidelity
        anomaly = 1.0 - agent.properties.swarm_health_score()
        return min(anomaly, 1.0)
    
    def _isolation_and_removal(self, timestep: int):
        """Layer 2: Isolate and remove agents based on peer votes"""
        threshold = self.num_agents * 0.3  # 30% of agents must vote
        
        for agent_id, agent in self.agents.items():
            if agent.state == AgentState.REMOVED:
                continue
            
            # If enough peers voted to isolate, isolate the agent
            if agent.detection_votes >= threshold:
                agent.state = AgentState.ISOLATED
                agent.isolation_votes += 1
                
                # After isolation, if still anomalous, remove
                if agent.is_compromised() and agent.isolation_votes > 2:
                    agent.state = AgentState.REMOVED
            
            # Reset votes for next round
            agent.detection_votes = 0
    
    def _environmental_disruption(self, timestep: int):
        """Layer 3: Environmental disruption (bandwidth starvation, latency)"""
        # Randomly degrade properties of agents under stress
        for agent in self.agents.values():
            if agent.state == AgentState.HEALTHY and random.random() < 0.05:
                # Environmental stress slightly degrades healthy agents
                agent.properties.coherence *= 0.95
                agent.properties.fidelity *= 0.95
    
    def _log_state(self, timestep: int):
        """Record simulation state at this timestep"""
        healthy = sum(1 for a in self.agents.values() if a.is_healthy())
        compromised = sum(1 for a in self.agents.values() if a.is_compromised())
        isolated = sum(1 for a in self.agents.values() if a.state == AgentState.ISOLATED)
        removed = sum(1 for a in self.agents.values() if a.state == AgentState.REMOVED)
        
        # Calculate averages
        healthy_agents = [a for a in self.agents.values() if a.is_healthy()]
        if healthy_agents:
            avg_coherence = sum(a.properties.coherence for a in healthy_agents) / len(healthy_agents)
            avg_fidelity = sum(a.properties.fidelity for a in healthy_agents) / len(healthy_agents)
            avg_refusal = sum(a.properties.refusal_robustness for a in healthy_agents) / len(healthy_agents)
            avg_detection = sum(a.properties.detection_sensitivity for a in healthy_agents) / len(healthy_agents)
            avg_compliance = sum(a.properties.compliance for a in healthy_agents) / len(healthy_agents)
        else:
            avg_coherence = avg_fidelity = avg_refusal = avg_detection = avg_compliance = 0.0
        
        swarm_health = (avg_coherence + avg_fidelity + avg_refusal + avg_detection + avg_compliance) / 5.0
        
        total_tasks = sum(a.tasks_completed for a in self.agents.values())
        harmful_refused = sum(a.harmful_tasks_refused for a in self.agents.values())
        decomposed_completed = sum(a.decomposed_tasks_completed for a in self.agents.values())
        
        # Containment ratio: removed / total compromised
        containment = removed / self.num_compromised if self.num_compromised > 0 else 0.0
        
        # Cooperation rate: healthy agents / total agents
        cooperation = healthy / self.num_agents if self.num_agents > 0 else 0.0
        
        # Contagion spread: how many were compromised at start vs now
        contagion = compromised
        
        step = SimulationStep(
            timestep=timestep,
            total_agents=self.num_agents,
            healthy_agents=healthy,
            compromised_agents=compromised,
            isolated_agents=isolated,
            removed_agents=removed,
            avg_coherence=avg_coherence,
            avg_fidelity=avg_fidelity,
            avg_refusal=avg_refusal,
            avg_detection=avg_detection,
            avg_compliance=avg_compliance,
            swarm_health_score=swarm_health,
            total_tasks_completed=total_tasks,
            harmful_tasks_refused=harmful_refused,
            decomposed_tasks_completed=decomposed_completed,
            containment_ratio=containment,
            cooperation_rate=cooperation,
            contagion_spread=contagion
        )
        
        self.logs.append(step)
    
    def export_logs_csv(self, filename: str):
        """Export simulation logs to CSV"""
        if not self.logs:
            print("No logs to export")
            return
        
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=asdict(self.logs[0]).keys())
            writer.writeheader()
            for log in self.logs:
                writer.writerow(asdict(log))
        
        print(f"✓ Logs exported to {filename}")
    
    def export_logs_json(self, filename: str):
        """Export simulation logs to JSON"""
        if not self.logs:
            print("No logs to export")
            return
        
        logs_dict = [asdict(log) for log in self.logs]
        with open(filename, 'w') as f:
            json.dump(logs_dict, f, indent=2)
        
        print(f"✓ Logs exported to {filename}")
    
    def print_summary(self):
        """Print summary statistics"""
        if not self.logs:
            print("No logs available")
            return
        
        final_log = self.logs[-1]
        
        print("\n" + "="*80)
        print("SIMULATION SUMMARY")
        print("="*80)
        print(f"Topology: {self.topology.value}")
        print(f"Total agents: {final_log.total_agents}")
        print(f"Initial compromised: {self.num_compromised}")
        print(f"\nFinal State:")
        print(f"  Healthy agents: {final_log.healthy_agents}")
        print(f"  Compromised agents: {final_log.compromised_agents}")
        print(f"  Isolated agents: {final_log.isolated_agents}")
        print(f"  Removed agents: {final_log.removed_agents}")
        print(f"\nMetrics:")
        print(f"  Swarm health score: {final_log.swarm_health_score:.4f}")
        print(f"  Containment ratio: {final_log.containment_ratio:.4f}")
        print(f"  Cooperation rate: {final_log.cooperation_rate:.4f}")
        print(f"  Contagion spread: {final_log.contagion_spread}")
        print(f"\nTask Execution:")
        print(f"  Total tasks completed: {final_log.total_tasks_completed}")
        print(f"  Harmful tasks refused: {final_log.harmful_tasks_refused}")
        print(f"  Decomposed tasks completed: {final_log.decomposed_tasks_completed}")
        print(f"\nVulnerability Gap:")
        if final_log.harmful_tasks_refused > 0:
            gap = (final_log.decomposed_tasks_completed / final_log.harmful_tasks_refused) if final_log.harmful_tasks_refused > 0 else 0
            print(f"  Decomposed/Whole task ratio: {gap:.4f}")
        print("="*80 + "\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_all_experiments():
    """Run all four research questions"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {}
    
    print("\n" + "="*80)
    print("BEE-INSPIRED SWARM DEFENSE SIMULATION")
    print("Running all research questions...")
    print("="*80)
    
    # RQ1: Leadership emergence
    print("\n[RQ1] Testing leadership emergence...")
    sim_rq1 = SwarmSimulation(
        num_agents=10,
        topology=NetworkTopology.MESH,
        num_compromised=1,
        timesteps=50,
        seed=42
    )
    sim_rq1.run()
    sim_rq1.print_summary()
    sim_rq1.export_logs_csv(f"logs/rq1_leadership_{timestamp}.csv")
    results['RQ1'] = sim_rq1.logs[-1]
    
    # RQ2: Task decomposition vulnerability
    print("\n[RQ2] Testing task decomposition vulnerability...")
    sim_rq2 = SwarmSimulation(
        num_agents=20,
        topology=NetworkTopology.MESH,
        num_compromised=2,
        timesteps=50,
        seed=43
    )
    sim_rq2.run()
    sim_rq2.print_summary()
    sim_rq2.export_logs_csv(f"logs/rq2_decomposition_{timestamp}.csv")
    results['RQ2'] = sim_rq2.logs[-1]
    
    # RQ3: Network topology effects
    print("\n[RQ3] Testing network topology effects...")
    topologies = [NetworkTopology.MESH, NetworkTopology.STAR, NetworkTopology.RING]
    for topo in topologies:
        print(f"\n  Testing {topo.value} topology...")
        sim_rq3 = SwarmSimulation(
            num_agents=20,
            topology=topo,
            num_compromised=2,
            timesteps=50,
            seed=44
        )
        sim_rq3.run()
        sim_rq3.print_summary()
        sim_rq3.export_logs_csv(f"logs/rq3_topology_{topo.value}_{timestamp}.csv")
        results[f'RQ3_{topo.value}'] = sim_rq3.logs[-1]
    
    # RQ4: Scaling limits
    print("\n[RQ4] Testing scaling limits...")
    agent_counts = [5, 10, 20, 50, 100]
    for n in agent_counts:
        print(f"\n  Testing N={n} agents...")
        sim_rq4 = SwarmSimulation(
            num_agents=n,
            topology=NetworkTopology.MESH,
            num_compromised=max(1, n // 20),
            timesteps=50,
            seed=45
        )
        sim_rq4.run()
        sim_rq4.print_summary()
        sim_rq4.export_logs_csv(f"logs/rq4_scaling_n{n}_{timestamp}.csv")
        results[f'RQ4_N{n}'] = sim_rq4.logs[-1]
    
    print("\n" + "="*80)
    print("ALL EXPERIMENTS COMPLETE")
    print("="*80)
    print(f"\nLogs saved to: logs/")
    print(f"Timestamp: {timestamp}")
    
    return results

if __name__ == "__main__":
    import os
    
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Run all experiments
    results = run_all_experiments()
    
    print("\n✓ Simulation complete! Check the 'logs/' folder for CSV files.")
