import sys
import os

# Adds the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from core.samplers.field_metropolis import field_local_update
from tqdm import tqdm

# Configuration
L = 32
lambd = 1.0
m_sq_range = np.linspace(-4.0, 0.5, 30)  # Scanning from broken to symmetric phase
n_sweeps = 10000
n_thermal = 2000
save_path = "data/processed/final_sweep_results.npy"


results = {
    "m_sq": m_sq_range,
    "mag": [],
    "chi": []
}

results_m = []

print("Starting Susceptibility Sweep...")


# --- The Monte Carlo Loop ---
for m_sq in m_sq_range:
    field = np.zeros((L, L))
    m_values = []
    
    for s in tqdm(range(n_sweeps), desc=f"m^2={m_sq:.2f}", leave=False):
        # Signature: field, m_sq, lambd, step_size, pot_type
        field_local_update(field, m_sq, lambd, 0.6, 0) # 0 for phi^4
        
        if s > n_thermal and s % 5 == 0: # Adding a small 'thinning' to reduce noise
            m_values.append(np.abs(np.mean(field)))
        
    # Calculate Observables
    m_avg = np.mean(m_values)
    chi = (L**2) * (np.mean(np.array(m_values)**2) - m_avg**2)
    
    results["mag"].append(m_avg)
    results["chi"].append(chi)
    print(f"m^2: {m_sq:.2f} | <|phi|>: {m_avg:.4f} | chi: {chi:.4f}")

# --- Plotting Results ---
fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.set_xlabel('$m^2$')
ax1.set_ylabel('Magnetization <|phi|>', color='tab:blue')
ax1.plot(m_sq_range, results["mag"], 'o-', color='tab:blue', label='Order Parameter')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Susceptibility (Fluctuations)', color='tab:red')
ax2.plot(m_sq_range, results["chi"], 's--', color='tab:red', label='Susceptibility')
ax2.tick_params(axis='y', labelcolor='tab:red')

plt.title("Phase Transition Sweep in $\phi^4$ Theory")
fig.tight_layout()
plt.grid(True, alpha=0.3)
plt.show()