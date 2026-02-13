import sys
import os

# Adds the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from core.samplers.field_metropolis import field_local_update
from core.samplers.wolff import wolff_update
from core.analysis import autocorrelation_function, estimate_tau

# Config
L = 16
m_sq = -3.29  # Your discovered critical point
lambd = 1.0
n_sweeps = 10000

# Containers
mag_metro = []
mag_wolff = []


# 1. Run Metropolis
field = np.zeros((L, L))
for _ in range(n_sweeps):
    # Updated signature: field, m_sq, lambd, step_size, pot_type
    field_local_update(field, m_sq, lambd, 0.6, 0) # 0 for phi^4
    mag_metro.append(np.mean(field))

# 2. Run Wolff
field = np.zeros((L, L))
for _ in range(n_sweeps):
    wolff_update(field, m_sq, lambd)
    mag_wolff.append(np.mean(field))

# Calculate Autocorrelations
rho_metro = autocorrelation_function(mag_metro)
rho_wolff = autocorrelation_function(mag_wolff)

# Plotting
plt.figure(figsize=(10, 5))
plt.plot(rho_metro[:500], label=f'Metropolis (tau ~ {estimate_tau(mag_metro):.1f})')
plt.plot(rho_wolff[:500], label=f'Wolff (tau ~ {estimate_tau(mag_wolff):.1f})')
plt.axhline(0, color='black', lw=1, ls='--')
plt.title("Autocorrelation Comparison at Criticality")
plt.xlabel("Lag (Sweeps)")
plt.ylabel("Correlation")
plt.legend()
plt.show()