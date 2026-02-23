# Path Integral Monte Carlo (PIMC) Simulator

My code to simulate 2D scalar field theories using Path Integral Monte Carlo and Lattice Field Theory techniques. This project implements sampling algorithms, including Numba-accelerated Metropolis-Hastings and the Wolff Cluster Update, to explore phenomena like quantum tunneling, symmetry breaking, and critical slowing down.

Read the full project report [here](https://drive.google.com/drive/folders/1sxZ6mpGKm9Dwxbkt_YwUhrzXC3EmhE3V?usp=sharing).

## Physics Overview

This simulator addresses two primary domains of physics:

1. **Quantum Mechanics (1D Path Integral)**: By mapping $(0+1)D$ quantum mechanics to a 1D statistical chain, we sample paths $x(\tau)$ with the weight $e^{-S_E/\hbar}$
   - Harmonic Oscillator: Validation against the analytical ground state $\psi_0(x)^2$.
   - Double Well: Observation of quantum tunneling and bimodal probability distributions.

2. **Scalar Field Theory ($\phi^4$)**: A 2D Euclidean lattice simulation of the $\phi^4$ model, used to study:
   - Spontaneous Symmetry Breaking: Transition from a symmetric phase ($m^2 > 0$) to a broken phase ($m^2 < 0$).
   - Phase Transitions: Scanning susceptibility $\chi$ and the order parameter $\langle|\phi|\rangle$.

## Features

- **High Performance**: Critical inner loops are optimized with Numba (JIT), providing near-C speeds for lattice updates.
- **Advanced Samplers**:
  - Metropolis-Hastings: Local updates for path and field configurations
  - Wolff Cluster Algorithm: A global update strategy that uses $Z_2$ reflection symmetry ($\phi \to -\phi$) to drastically reduce critical slowing down.
- **Analysis Suite**: Tools for calculating spatial correlations $G(r)$, integrated autocorrelation time $\tau_{int}$, and susceptibility.

## Getting Started

### Prerequisites

- Install [Python 3.11+](https://www.python.org/downloads). This project relies on NumPy, SciPy, Matplotlib, tqdm, and Numba declared in `requirements.txt`.
- Available RAM of $>8\text{GB}$ is recommended for the larger Phi-4 sweeps.

### Setup

```bash
# Clone the repository
git clone https://github.com/samreetdhillon/path-integral-simulator.git
cd path-integral-simulator
# create virtual environment
python -m venv venv
# activate virtual environment
venv\Scripts\activate
# Install required libraries
pip install -r requirements.txt
```

### Running Experiments

```bash
# Quantum Harmonic Oscillator
python -m experiments.run_qho
# Double-Well Tunneling
python -m experiments.run_double_well
# Phi-4 Field Dynamics
python -m experiments.run_phi4
# Phase Transition Sweep
python -m experiments.run_sweep
# Sampler Comparison
python -m experiments.metropolis_vs_wolff
```

You can adjust lattice sizes, couplings, and step sizes through the script-level constants near the top of each module.

## Tests

I've also included a suite of tests to ensure the potentials and lattice geometries are handled correctly:

```bash
python tests/test_physics.py
```
