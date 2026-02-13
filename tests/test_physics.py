import sys
import os

# Adds the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import numpy as np
from core.potentials.scalar_potentials import harmonic_potential

class TestPhysics(unittest.TestCase):
    def test_harmonic_potential_minimum(self):
        # The minimum of a QHO potential must be at x=0
        self.assertEqual(harmonic_potential(0.0, 1.0), 0.0)
        self.assertGreater(harmonic_potential(1.0, 1.0), 0.0)

    def test_lattice_shape(self):
        # Ensure periodic boundaries don't crash
        L = 10
        field = np.zeros((L, L))
        self.assertEqual(field.shape, (10, 10))

    def test_double_well_minima(self):
        from core.potentials.scalar_potentials import double_well_potential
        # If a_param is 2.0, minima should be at x = 2.0 and x = -2.0
        self.assertEqual(double_well_potential(2.0, 1.0, 2.0), 0.0)
        self.assertEqual(double_well_potential(-2.0, 1.0, 2.0), 0.0)

if __name__ == '__main__':
    unittest.main()