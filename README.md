# Path Integral Monte Carlo (PIMC) Simulator

A modular physics suite that discretizes Euclidean path integrals for quantum systems and scalar field theories, solves them with optimized Markov chain Monte Carlo kernels, and packages the diagnostics as reproducible plots in assets/.

## Overview

We simulate three archetypal non-perturbative systems—Quantum Harmonic Oscillator (QHO), Phi-4 field theory, and a double-well potential—by sampling the Euclidean path integral in one or two dimensions. The toolkit blends local Metropolis updates and cluster Wolff flips with a compact analysis module so you can study spontaneous symmetry breaking, critical slowing down, and quantum tunneling without leaving Python.

## Problem Statement

- **Quantum regimes** require sampling from high-dimensional, non-Gaussian distributions whose dominant configurations are dictated by competing kinetic and potential parts of the Euclidean action.
- **Critical slowing down** near second-order phase transitions makes naive Metropolis updates inefficient; correlated sweeps are expensive to interpret quantitatively.
- **Physical intuition** demands diagnostics such as magnetization, susceptibility, autocorrelations, and revival of analytic results (e.g., ground-state wavefunctions) to validate the sampling engine.

## Solution

1. **Discretized Action** — The project encodes lattice versions of the kinetic term plus scalar potentials in core/potentials/scalar_potentials.py, covering harmonic, Phi-4, and double-well wells with Numba-accelerated calls.
2. **Sampler Library** — Local updates (`core.samplers.metropolis.local_update`) sweep the Euclidean time path, `core.samplers.field_metropolis.field_local_update` generalizes to 2D lattices, and `core.samplers.wolff.wolff_update` implements a reflection-based cluster update that shrinks $ au\_{int}$ near criticality.
3. **Statistical Toolbox** — `core.analysis` provides spatial autocorrelations, normalized time-series correlations, and integrated autocorrelation estimates (`estimate_tau`) so runs can be analyzed for ergodicity and efficiency.

### Methodology Details

- **Potentials**: `phi4_potential` blends mass-squared and quartic couplings for spontaneous symmetry breaking, `harmonic_potential` matches analytic QHO behavior, and `double_well_potential` exposes barrier crossing physics.
- **Local Metropolis**: Proposals add uniform noise then accept with Boltzmann weights that combine nearest-neighbor kinetic estimates with the relevant potential from the dispatcher in `core.samplers.metropolis`.
- **Field Updates**: 2D lattices adopt periodic boundaries; updates compute optimized kinetic differences and potential deltas to keep acceptance rates stable across regimes.
- **Cluster Moves**: Wolff flips use stack-based growth and bond probabilities that favor same-sign neighbors, enabling entire clusters to reflect and collapse autocorrelations near the phase transition point $m^2\approx -3.3$.
- **Analysis**: Autocorrelation curves and integrated $ au$ values highlight how Wolff out-performs Metropolis empirically for magnetization time-series, with utility functions automatically normalizing and windowing.

## Experiments & Results

| Script                                      | Purpose                                                                                                                   | Key Observable                                             | Plot                                             |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------- | ------------------------------------ |
| `python -m experiments.run_qho`             | Validate the PIMC QHO ground-state density against the analytic $ ext{e}^{-x^2}$ curve.                                   | Sampled probability density along the Euclidean time mesh. | [assets/qho.png](assets/qho.png)                 |
| `python -m experiments.run_double_well`     | Demonstrate tunneling-induced bimodality.                                                                                 | Histogram of sampled positions with two peaks at $\\pm a$. | [assets/double-well.png](assets/double-well.png) |
| `python -m experiments.run_phi4`            | Visualize instant field configurations and time-series magnetization in Phi-4 theory.                                     | Spatial snapshot + order parameter trace.                  | [assets/phi4.png](assets/phi4.png)               |
| `python -m experiments.run_sweep`           | Sweep $m^2$ to locate susceptibility spikes signalling symmetry breaking; saves `data/processed/final_sweep_results.npy`. | Order parameter $\\<                                       | \phi                                             | \> $ and susceptibility $\\chi$ across $m^2$ values. | [assets/sweep.png](assets/sweep.png) |
| `python -m experiments.metropolis_vs_wolff` | Compare autocorrelations of phi4 magnetization at the critical point.                                                     | Normalized autocorrelation curves, integrated $ au$.       | [assets/comparison.png](assets/comparison.png)   |

The plots under assets/ document key physics: [assets/sweep.png](assets/sweep.png) captures the susceptibility peak ($m^2 \approx -3.3$), [assets/comparison.png](assets/comparison.png) shows Wolff collapsing the autocorrelation time from $ au\approx132$ to order one, and the histogram plots validate tunneling and ground-state behavior.

## Getting Started

### Prerequisites

- Install [Python 3.11+](https://www.python.org/downloads). This project relies on NumPy, SciPy, Matplotlib, tqdm, and Numba declared in `requirements.txt`.
- Available RAM of $>8\text{GB}$ is recommended for the larger Phi-4 sweeps.

### Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Running Experiments

1. **Quantum Harmonic Oscillator**: `python -m experiments.run_qho`
2. **Double-Well Tunneling**: `python -m experiments.run_double_well`
3. **Phi-4 Field Dynamics**: `python -m experiments.run_phi4`
4. **Phase Transition Sweep**: `python -m experiments.run_sweep` (writes `data/processed/final_sweep_results.npy`)
5. **Sampler Comparison**: `python -m experiments.metropolis_vs_wolff`

Adjust lattice sizes, couplings, and step sizes through the script-level constants near the top of each module.

## Data & Outputs

- `data/processed/` stores NumPy arrays produced by sweeps (currently `final_sweep_results.npy`).
- `assets/` collects Matplotlib figures that illustrate the phenomena above. Use the PNG files in reports or presentations; regeneration is as simple as re-running the corresponding experiment script.

## Tests

```bash
python -m unittest tests/test_physics.py
```

The unit tests ensure the scalar potentials and lattice shapes remain anchored to the expected minima and boundary conditions described in `core/potentials/scalar_potentials.py`.

## Project Layout

- `core/` – Samplers (`field_metropolis.py`, `metropolis.py`, `wolff.py`), potentials, and analysis utilities.
- `experiments/` – High-level scripts for each physics story.
- `data/` – Raw and processed numerical outputs.
- `assets/` – Static plot artifacts referenced above.
- `tests/` – Minimal regression guardrails for the physics kernels.

## Next Steps

1. Extend `core.samplers.field_metropolis` to support anisotropic lattices for 3D studies.
2. Add temperature-dependent runs and metadata logging for reproducibility.
3. Export data/processed results to CSV for downstream plotting pipelines.
