import numpy as np
from numba import njit

@njit
def phi4_potential(phi, m_sq, lambd):
    return (m_sq / 2) * (phi**2) + (lambd / 4) * (phi**4)

@njit
def harmonic_potential(x, m, omega=1.0):
    return 0.5 * m * (omega**2) * (x**2)

@njit
def double_well_potential(phi, V0, a_param):
    return V0 * ((phi**2 - a_param**2)**2)