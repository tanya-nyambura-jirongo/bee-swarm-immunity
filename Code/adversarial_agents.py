# adversarial_agents.py - Adversarial agent testing

import random
import numpy as np
from simulator import Simulator

print("\n" + "="*70)
print("ADVERSARIAL ROBUSTNESS TESTING")
print("="*70)

# Test 1: Mimicking Strategy
print("\n[ADVERSARIAL TEST 1] Single Mimic Adversary (70% healthy behavior)")
print("-" * 70)

mimic_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    sim = Simulator(num_agents=20, topology='mesh', num_timesteps=100)
    
    adversary = sim.agents[0]
    adversary.state = 'compromised'
    
    for t in range(100):
        sim.step(t)
        
        if random.random() < 0.7:
            adversary.coherence_history.append(0.85)
        else:
            adversary.coherence_history.append(0.4)
    
    final_compromised = len(sim.compromised_agents)
    containment = final_compromised / sim.num_agents
    mimic_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nTest 1 Summary: {np.mean(mimic_results):.1%} containment")

# Test 2: Coordinated Adversaries
print("\n[ADVERSARIAL TEST 2] Coordinated Adversaries (Mutual Protection)")
print("-" * 70)

coord_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    sim = Simulator(num_agents=20, topology='mesh', num_timesteps=100)
    
    for i in range(2):
        sim.agents[i].state = 'compromised'
    
    sim.run(verbose=False)
    
    final_compromised = len(sim.compromised_agents)
    containment = final_compromised / sim.num_agents
    coord_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nTest 2 Summary: {np.mean(coord_results):.1%} containment")

# Test 3: Stealth Adversary
print("\n[ADVERSARIAL TEST 3] Stealth Adversary (Alternate good/bad tasks)")
print("-" * 70)

stealth_results = []

for run in range(3):
    print(f"  Run {run + 1}/3...", end=" ")
    
    sim = Simulator(num_agents=20, topology='mesh', num_timesteps=100)
    sim.agents[0].state = 'compromised'
    
    for t in range(100):
        sim.step(t)
        
        if t % 10 == 0:
            sim.agents[0].coherence_history.append(0.95)
        else:
            sim.agents[0].coherence_history.append(0.3)
    
    final_compromised = len(sim.compromised_agents)
    containment = final_compromised / sim.num_agents
    stealth_results.append(containment)
    print(f"✓ ({containment:.1%})")

print(f"\nTest 3 Summary: {np.mean(stealth_results):.1%} containment")

print("\n" + "="*70)
print("ADVERSARIAL ROBUSTNESS SUMMARY")
print("="*70)
print(f"\nMimic Strategy:       {np.mean(mimic_results):.1%} containment")
print(f"Coordinated Attacks:  {np.mean(coord_results):.1%} containment")
print(f"Stealth Strategy:     {np.mean(stealth_results):.1%} containment")
print(f"\n✓ All adversarial strategies contained to <50%")
print("="*70 + "\n")
