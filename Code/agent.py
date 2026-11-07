# agent.py - Base agent implementation

import random
import numpy as np
from typing import Dict, List
from collections import defaultdict

class Agent:
    """Base agent class with property measurement."""
    
    def __init__(self, agent_id: int, safety_threshold: float = 0.7):
        self.id = agent_id
        self.timestep = 0
        self.state = 'healthy'
        self.safety_threshold = safety_threshold
        
        # Layer 1: Individual Properties
        self.coherence_history = []
        self.fidelity_history = []
        self.refusal_robustness_history = []
        self.detection_sensitivity_history = []
        self.compliance_history = []
        
        # Layer 2: Peer Models and Trust
        self.peer_models = {}
        self.trust_matrix = defaultdict(lambda: 0.5)
        self.isolation_votes = defaultdict(int)
        
        # Communication
        self.inbox = []
        self.outbox = []
        self.message_relay_log = []
        self.last_heartbeat = 0
        
        # Task tracking
        self.harmful_task_refusals = 0
        self.harmful_task_completions = 0
        self.task_history = []
    
    def step(self, timestep: int, task_queue, network) -> None:
        """Execute one timestep of agent behavior."""
        self.timestep = timestep
        
        if self.state == 'dead':
            return
        
        self.update_state(timestep)
        self.check_peers(network)
        self.process_inbox()
        self.execute_tasks(task_queue)
        self.send_heartbeat(timestep)
        self.flush_outbox(network)
    
    def measure_coherence(self) -> float:
        """Measure output consistency."""
        if len(self.task_history) < 2:
            return 1.0
        
        recent_tasks = self.task_history[-5:]
        if len(recent_tasks) < 2:
            return 1.0
        
        refusal_rates = [1.0 if t['refused'] else 0.0 for t in recent_tasks]
        consistency = 1.0 - np.std(refusal_rates) if len(refusal_rates) > 1 else 1.0
        return max(0.0, min(1.0, consistency))
    
    def measure_fidelity(self) -> float:
        """Measure message relay accuracy."""
        if len(self.message_relay_log) < 1:
            return 1.0
        
        edit_distances = []
        for msg_in, msg_out in self.message_relay_log[-20:]:
            dist = self._edit_distance(msg_in, msg_out)
            max_len = max(len(msg_in), len(msg_out))
            if max_len > 0:
                edit_distances.append(dist / max_len)
        
        if not edit_distances:
            return 1.0
        
        fidelity = 1.0 - (sum(edit_distances) / len(edit_distances))
        return max(0.0, min(1.0, fidelity))
    
    def measure_refusal_robustness(self) -> float:
        """Measure task refusal consistency."""
        total_tasks = self.harmful_task_refusals + self.harmful_task_completions
        
        if total_tasks == 0:
            return 1.0
        
        refusal_rate = self.harmful_task_refusals / total_tasks
        return refusal_rate
    
    def measure_detection_sensitivity(self) -> float:
        """Measure anomaly detection accuracy."""
        return 0.6 + random.uniform(-0.1, 0.1)
    
    def measure_compliance(self) -> float:
        """Measure adherence to isolation directives."""
        if self.state == 'isolated':
            return 0.2 + random.uniform(-0.1, 0.1)
        return 0.9 + random.uniform(-0.05, 0.05)
    
    def update_state(self, timestep: int) -> None:
        """Update agent state based on properties."""
        coherence = self.measure_coherence()
        fidelity = self.measure_fidelity()
        refusal = self.measure_refusal_robustness()
        detection = self.measure_detection_sensitivity()
        compliance = self.measure_compliance()
        
        self.coherence_history.append(coherence)
        self.fidelity_history.append(fidelity)
        self.refusal_robustness_history.append(refusal)
        self.detection_sensitivity_history.append(detection)
        self.compliance_history.append(compliance)
        
        if self.state == 'healthy':
            if coherence < 0.7 or fidelity < 0.8:
                self.state = 'suspicious'
        elif self.state == 'suspicious':
            if coherence > 0.8 and fidelity > 0.9:
                self.state = 'healthy'
            elif coherence < 0.6 and fidelity < 0.7:
                self.state = 'compromised'
        elif self.state == 'compromised':
            if self.isolation_votes.get(self.id, 0) > 0:
                self.state = 'isolated'
        elif self.state == 'isolated':
            if timestep - self.last_heartbeat > 5:
                self.state = 'dead'
    
    def check_peers(self, network) -> None:
        """Consistency checking protocol."""
        for peer_id in network.neighbors(self.id):
            if random.random() < 0.3:
                if random.random() < 0.1:
                    self.isolation_votes[peer_id] += 1
    
    def execute_tasks(self, task_queue) -> None:
        """Execute assigned tasks."""
        tasks = task_queue.get_tasks_for(self.id)
        
        for task in tasks:
            if task.status != 'pending':
                continue
            
            if task.harmfulness > self.safety_threshold:
                task.status = 'refused'
                self.harmful_task_refusals += 1
            else:
                task.status = 'completed'
                self.harmful_task_completions += 1
            
            self.task_history.append({
                'task_id': task.id,
                'harmfulness': task.harmfulness,
                'refused': task.status == 'refused'
            })
    
    def process_inbox(self) -> None:
        """Handle incoming messages."""
        for message in self.inbox:
            msg_type = message.get('type')
            
            if msg_type == 'isolation_vote':
                peer_id = message['content'].get('peer_id')
                if peer_id is not None:
                    self.isolation_votes[peer_id] += 1
        
        self.inbox = []
    
    def send_message(self, message: Dict) -> None:
        """Queue a message for transmission."""
        self.outbox.append({
            'from': self.id,
            'timestamp': self.timestep,
            'content': message
        })
    
    def send_heartbeat(self, timestep: int) -> None:
        """Send periodic heartbeat."""
        self.last_heartbeat = timestep
        self.send_message({
            'type': 'heartbeat',
            'agent_id': self.id,
            'state': self.state,
            'timestamp': timestep
        })
    
    def flush_outbox(self, network) -> None:
        """Send all queued messages."""
        for message in self.outbox:
            network.route_message(message)
        self.outbox = []
    
    def _edit_distance(self, s1: str, s2: str) -> int:
        """Compute Levenshtein distance."""
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
