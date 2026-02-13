import numpy as np
from numba import njit

@njit
def wolff_update(field, m_sq, lambd):
    """
    Optimized Wolff Cluster Update for Phi^4 and Double Well theories.
    Uses the Z2 reflection (phi -> -phi).
    """
    L_x, L_t = field.shape
    i, j = np.random.randint(0, L_x), np.random.randint(0, L_t)
    
    # We use a stack for the cluster growth (to avoid recursion depth issues)
    cluster_stack = [(i, j)]
    visited = np.zeros((L_x, L_t), dtype=np.int8)
    visited[i, j] = 1
    
    while len(cluster_stack) > 0:
        curr_i, curr_j = cluster_stack.pop()
        phi_curr = field[curr_i, curr_j]
        
        for di, dj in [(0,1), (0,-1), (1,0), (-1,0)]:
            ni, nj = (curr_i + di) % L_x, (curr_j + dj) % L_t
            
            if not visited[ni, nj]:
                phi_neigh = field[ni, nj]
                
                # The bond probability logic:
                # Clusters grow between sites that have the same sign.
                # If phi_curr * phi_neigh > 0, they are on the same side of the well.
                force = 2.0 * phi_curr * phi_neigh
                if force > 0:
                    p = 1.0 - np.exp(-force)
                    if np.random.random() < p:
                        visited[ni, nj] = 1
                        cluster_stack.append((ni, nj))
    
    # Flip the entire cluster (phi -> -phi)
    for r in range(L_x):
        for c in range(L_t):
            if visited[r, c]:
                field[r, c] *= -1.0
                
    return np.sum(visited)