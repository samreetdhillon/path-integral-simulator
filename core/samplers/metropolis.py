import numpy as np
from numba import njit
from core.potentials.scalar_potentials import phi4_potential, harmonic_potential, double_well_potential

@njit
def local_update(path, a, m, thermal_step_size, pot_type=0, lambd=0.0, V0=1.0, a_dw=1.5):
    """
    pot_type: 0 for phi4/harmonic, 1 for double_well
    lambd: used if pot_type=0
    V0, a_dw: used if pot_type=1
    """
    N = len(path)
    accepted = 0
    
    for i in range(N):
        prev_i = (i - 1) % N
        next_i = (i + 1) % N
        
        old_x = path[i]
        new_x = old_x + np.random.uniform(-thermal_step_size, thermal_step_size)
        
        # Kinetic Term (Universal)
        diff_old = (path[next_i] - old_x)**2 + (old_x - path[prev_i])**2
        diff_new = (path[next_i] - new_x)**2 + (new_x - path[prev_i])**2
        dS_kinetic = (m / (2 * a)) * (diff_new - diff_old)
        
        # Potential Term Dispatcher
        if pot_type == 0:
            # Covers Harmonic (lambd=0) and Phi4
            v_new = phi4_potential(new_x, m**2, lambd)
            v_old = phi4_potential(old_x, m**2, lambd)
        else:
            # Double Well
            v_new = double_well_potential(new_x, V0, a_dw)
            v_old = double_well_potential(old_x, V0, a_dw)
            
        dS = dS_kinetic + a * (v_new - v_old)
        
        if dS <= 0 or np.exp(-dS) > np.random.random():
            path[i] = new_x
            accepted += 1
            
    return accepted / N