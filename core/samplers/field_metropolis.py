import numpy as np
from numba import njit
from core.potentials.scalar_potentials import phi4_potential, double_well_potential

@njit
def field_local_update(field, m_sq, lambd, step_size, pot_type=0, V0=1.0, a_dw=1.5):
    """
    Updates a 2D scalar field lattice using Metropolis-Hastings.
    pot_type: 0 for phi4, 1 for double_well
    """
    L_x, L_t = field.shape
    accepted = 0
    
    for i in range(L_x):
        for j in range(L_t):
            old_phi = field[i, j]
            new_phi = old_phi + np.random.uniform(-step_size, step_size)
            
            # Identify neighbors with Periodic Boundary Conditions
            sum_neigh = field[(i + 1) % L_x, j] + \
                        field[(i - 1) % L_x, j] + \
                        field[i, (j + 1) % L_t] + \
                        field[i, (j - 1) % L_t]
            
            # Optimized Kinetic Term
            dS_kinetic = (new_phi**2 - old_phi**2)*2 - (new_phi - old_phi)*sum_neigh
            
            # Potential Term Dispatcher
            if pot_type == 0:
                v_new = phi4_potential(new_phi, m_sq, lambd)
                v_old = phi4_potential(old_phi, m_sq, lambd)
            else:
                v_new = double_well_potential(new_phi, V0, a_dw)
                v_old = double_well_potential(old_phi, V0, a_dw)
            
            dS = dS_kinetic + v_new - v_old
            
            if dS <= 0 or np.exp(-dS) > np.random.random():
                field[i, j] = new_phi
                accepted += 1
                
    return accepted / (L_x * L_t)