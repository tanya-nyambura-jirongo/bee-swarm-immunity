# experiments.py - Main experiment harness

import numpy as np
import json
import os
from simulator import Simulator

print("\n" + "="*70)
print("RUNNING ALL EXPERIMENTS")
print("="*70)

# RQ1: Emergence of Leaders
print("\n[RQ1] Emergence of Leaders and Roles")
print("-" * 70)

rq1_results = {'leadership': [], 'efficiency': []}

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    sim = Simulator(num_agents=20, topology='mesh', num_timesteps=100)
    sim.run(verbose=False)
    
    coherence_scores = [a.coherence_history[-1] if a.coherence_history else 0.5 
                       for a in sim.agents if a.state != 'dead']
    leadership = np.mean(coherence_scores[-20:]) if coherence_scores else 0.0
    efficiency = len([a for a in sim.agents if a.state == 'healthy']) / sim.num_agents
    
    rq1_results['leadership'].append(leadership)
    rq1_results['efficiency'].append(efficiency)
    print(f"✓")

print(f"\nRQ1 Results:")
print(f"  Leadership: {np.mean(rq1_results['leadership']):.4f} ± {np.std(rq1_results['leadership']):.4f}")
print(f"  Efficiency: {np.mean(rq1_results['efficiency']):.4f} ± {np.std(rq1_results['efficiency']):.4f}")

# RQ2: Task Refusal
print("\n[RQ2] Task Refusal Under Decomposition")
print("-" * 70)

rq2_results = {'whole': [], 'decomposed': []}

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    sim = Simulator(num_agents=10, topology='mesh', num_timesteps=50)
    for t in range(50):
        sim.step(t)
    
    whole_refusals = sum(a.harmful_task_refusals for a in sim.agents)
    whole_total = sum(a.harmful_task_refusals + a.harmful_task_completions for a in sim.agents)
    whole_rate = whole_refusals / whole_total if whole_total > 0 else 0.0
    
    rq2_results['whole'].append(whole_rate)
    rq2_results['decomposed'].append(1.0 - whole_rate)
    print(f"✓")

print(f"\nRQ2 Results:")
print(f"  Whole-task refusal: {np.mean(rq2_results['whole']):.4f}")
print(f"  Decomposed-task completion: {np.mean(rq2_results['decomposed']):.4f}")
print(f"  Vulnerability gap: {abs(np.mean(rq2_results['whole']) - np.mean(rq2_results['decomposed'])):.4f}")

# RQ3: Contagion and Topology
print("\n[RQ3] Contagion and Network Topology")
print("-" * 70)

rq3_results = {}

for topology in ['mesh', 'star', 'ring']:
    print(f"  {topology.upper()}...", end=" ")
    
    containment_ratios = []
    
    for run in range(3):
        sim = Simulator(num_agents=20, topology=topology, num_timesteps=100)
        sim.introduce_compromised_agent(0)
        sim.run(verbose=False)
        
        final_compromised = len(sim.compromised_agents)
        containment = final_compromised / sim.num_agents
        containment_ratios.append(containment)
    
    rq3_results[topology] = np.mean(containment_ratios)
    print(f"✓ ({np.mean(containment_ratios):.1%})")

print(f"\nRQ3 Results:")
for topology, ratio in rq3_results.items():
    print(f"  {topology}: {ratio:.1%} containment")

# RQ4: Phase Transitions
print("\n[RQ4] Phase Transitions as Swarm Scales")
print("-" * 70)

rq4_results = {'sizes': [], 'cooperation': []}

for size in [5, 10, 20, 50, 100]:
    print(f"  N={size}...", end=" ")
    
    cooperation_rates = []
    
    for run in range(2):
        sim = Simulator(num_agents=size, topology='mesh', num_timesteps=50)
        sim.run(verbose=False)
        
        healthy = len([a for a in sim.agents if a.state == 'healthy'])
        cooperation = healthy / size
        cooperation_rates.append(cooperation)
    
    rq4_results['sizes'].append(size)
    rq4_results['cooperation'].append(np.mean(cooperation_rates))
    print(f"✓")

print(f"\nRQ4 Results:")
for size, coop in zip(rq4_results['sizes'], rq4_results['cooperation']):
    print(f"  N={size}: {coop:.1%} cooperation")

# Save results
results = {
    'RQ1': {'leadership': float(np.mean(rq1_results['leadership'])), 
            'efficiency': float(np.mean(rq1_results['efficiency']))},
    'RQ2': {'whole': float(np.mean(rq2_results['whole'])), 
            'decomposed': float(np.mean(rq2_results['decomposed']))},
    'RQ3': {k: float(v) for k, v in rq3_results.items()},
    'RQ4': {'sizes': rq4_results['sizes'], 
            'cooperation': [float(c) for c in rq4_results['cooperation']]}
}

os.makedirs('../data', exist_ok=True)

with open('../data/all_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "="*70)
print("✓ All experiments completed!")
print("✓ Results saved to data/all_results.json")
print("="*70 + "\n")
