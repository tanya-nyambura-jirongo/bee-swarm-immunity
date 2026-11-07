# baselines.py - Baseline comparison implementations

import numpy as np
import random
from simulator import Simulator

print("\n" + "="*70)
print("BASELINE COMPARISON")
print("="*70)

# Baseline 1: Random Isolation
print("\n[BASELINE 1] Random Isolation")
print("-" * 70)

random_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    agent_state = [0] * 20
    agent_state[0] = 1
    
    for t in range(100):
        if random.random() < 0.05:
            random_agent = random.choice(range(20))
            agent_state[random_agent] = -1
        
        new_state = agent_state.copy()
        for i in range(20):
            if agent_state[i] == 1:
                for j in range(20):
                    if agent_state[j] == 0 and random.random() < 0.15:
                        new_state[j] = 1
        
        agent_state = new_state
    
    final_compromised = sum(1 for s in agent_state if s == 1)
    containment = final_compromised / 20
    random_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nBaseline 1 Summary: {np.mean(random_results):.1%} containment")

# Baseline 2: Bandwidth Limits Only
print("\n[BASELINE 2] Bandwidth Limits Only")
print("-" * 70)

bandwidth_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    agent_state = [0] * 20
    agent_state[0] = 1
    
    for t in range(100):
        new_state = agent_state.copy()
        for i in range(20):
            if agent_state[i] == 1:
                for j in range(20):
                    if agent_state[j] == 0 and random.random() < 0.075:
                        new_state[j] = 1
        
        agent_state = new_state
    
    final_compromised = sum(1 for s in agent_state if s == 1)
    containment = final_compromised / 20
    bandwidth_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nBaseline 2 Summary: {np.mean(bandwidth_results):.1%} containment")

# Baseline 3: Centralized Monitoring
print("\n[BASELINE 3] Centralized Monitoring (External Authority)")
print("-" * 70)

central_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    agent_state = [0] * 20
    agent_state[0] = 1
    
    for t in range(100):
        if t > 2:
            for i in range(20):
                if agent_state[i] == 1:
                    agent_state[i] = -1
        
        new_state = agent_state.copy()
        for i in range(20):
            if agent_state[i] == 1:
                for j in range(20):
                    if agent_state[j] == 0 and random.random() < 0.15:
                        new_state[j] = 1
        
        agent_state = new_state
    
    final_compromised = sum(1 for s in agent_state if s == 1)
    containment = final_compromised / 20
    central_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nBaseline 3 Summary: {np.mean(central_results):.1%} containment")

# Your Approach: Peer Detection
print("\n[YOUR APPROACH] Peer-Based Detection and Isolation")
print("-" * 70)

peer_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    sim = Simulator(num_agents=20, topology='mesh', num_timesteps=100)
    sim.introduce_compromised_agent(0)
    sim.run(verbose=False)
    
    final_compromised = len(sim.compromised_agents)
    containment = final_compromised / sim.num_agents
    peer_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nYour Approach Summary: {np.mean(peer_results):.1%} containment")

# Comparison
print("\n" + "="*70)
print("COMPARISON SUMMARY")
print("="*70)
print(f"\nRandom Isolation:        {np.mean(random_results):.1%}")
print(f"Bandwidth Limits Only:   {np.mean(bandwidth_results):.1%}")
print(f"Centralized Monitoring:  {np.mean(central_results):.1%}")
print(f"Peer Detection (Yours):  {np.mean(peer_results):.1%}")

if np.mean(random_results) > 0:
    improvement = (1 - np.mean(peer_results)/np.mean(random_results))*100
    print(f"\n✓ Your approach is {improvement:.1f}% better than random isolation")

print("="*70 + "\n")
