# this file is AI-generated via GitHub Copilot,
# It is meant to be a user-friendly wrapper around the core PIMC experiments I created,
# allowing users to configure parameters and run simulations without editing code.

"""Command-line interface that wraps the existing PIMC experiments."""

from __future__ import annotations

from typing import Any, Callable, Dict

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from core.analysis import autocorrelation_function, estimate_tau
from core.samplers.field_metropolis import field_local_update
from core.samplers.metropolis import local_update
from core.samplers.wolff import wolff_update

WELCOME_TEXT = """
Welcome to the Path Integral Monte Carlo (PIMC) companion.
This interactive wrapper lets you choose a popular physics story, tune
its lattice parameters, and then see the result without editing scripts.
"""


def prompt_numeric(
    prompt_message: str,
    default,
    cast: Callable,
    validator: Callable[[Any], bool] | None = None,
    validator_msg: str | None = None,
):
    """Ask the user for a numeric value and fall back to the default."""
    while True:
        raw = input(f"{prompt_message} [{default}]: ").strip()
        if raw == "":
            value = default
        else:
            try:
                value = cast(raw)
            except ValueError:
                print(f"Please enter a valid {cast.__name__}.")
                continue
        if validator and not validator(value):
            print(validator_msg or "Value does not meet requirements.")
            continue
        return value


def gather_qho_parameters() -> Dict[str, float | int]:
    print("\nConfiguring the Quantum Harmonic Oscillator run")
    return {
        "N": prompt_numeric("Number of lattice sites (N)", 100, int, lambda x: x > 0, "Must be positive."),
        "a": prompt_numeric("Lattice spacing (a)", 0.5, float, lambda x: x > 0, "Must be positive."),
        "m": prompt_numeric("Mass (m)", 1.0, float, lambda x: x > 0, "Must be positive."),
        "omega": prompt_numeric("Oscillator frequency (omega)", 1.0, float, lambda x: x > 0, "Must be positive."),
        "step_size": prompt_numeric("Proposal width", 1.5, float, lambda x: x > 0, "Must be positive."),
        "n_sweeps": prompt_numeric("Total Monte Carlo sweeps", 50000, int, lambda x: x > 0, "Must be positive."),
        "n_thermal": prompt_numeric("Thermalization sweeps", 5000, int, lambda x: x >= 0, "Cannot be negative."),
        "collect_every": prompt_numeric("Record data every N sweeps", 10, int, lambda x: x > 0, "Must be positive."),
        "lambda_poly": prompt_numeric("Quartic coupling (lambda)", 0.0, float, lambda x: x >= 0, "Cannot be negative."),
    }


def gather_double_well_parameters() -> Dict[str, float | int]:
    print("\nConfiguring the Double-Well tunneling run")
    return {
        "N": prompt_numeric("Number of lattice sites", 100, int, lambda x: x > 0, "Must be positive."),
        "a": prompt_numeric("Lattice spacing (a)", 0.5, float, lambda x: x > 0, "Must be positive."),
        "m": prompt_numeric("Mass (m)", 1.0, float, lambda x: x > 0, "Must be positive."),
        "V0": prompt_numeric("Barrier height (V0)", 0.5, float, lambda x: x > 0, "Must be positive."),
        "a_param": prompt_numeric("Double-well minima location (a)", 2.0, float, lambda x: x > 0, "Must be positive."),
        "step_size": prompt_numeric("Proposal width", 1.5, float, lambda x: x > 0, "Must be positive."),
        "n_sweeps": prompt_numeric("Total Monte Carlo sweeps", 100000, int, lambda x: x > 0, "Must be positive."),
        "n_thermal": prompt_numeric("Thermalization sweeps", 5000, int, lambda x: x >= 0, "Cannot be negative."),
        "collect_every": prompt_numeric("Record data every N sweeps", 10, int, lambda x: x > 0, "Must be positive."),
    }


def gather_phi4_parameters() -> Dict[str, float | int]:
    print("\nConfiguring the Phi^4 field theory run")
    return {
        "L": prompt_numeric("Field lattice dimension (L)", 32, int, lambda x: x > 0, "Must be positive."),
        "lambd": prompt_numeric("Quartic coupling (lambda)", 1.0, float, lambda x: x >= 0, "Cannot be negative."),
        "m_sq": prompt_numeric("Mass squared (m^2)", -2.0, float),
        "step_size": prompt_numeric("Proposal width", 0.5, float, lambda x: x > 0, "Must be positive."),
        "n_sweeps": prompt_numeric("Total Monte Carlo sweeps", 10000, int, lambda x: x > 0, "Must be positive."),
        "n_thermal": prompt_numeric("Thermalization sweeps", 1000, int, lambda x: x >= 0, "Cannot be negative."),
        "collect_every": prompt_numeric("Record data every N sweeps", 5, int, lambda x: x > 0, "Must be positive."),
    }


def gather_sweep_parameters() -> Dict[str, float | int]:
    print("\nConfiguring the Phi^4 susceptibility sweep")
    m_sq_min = prompt_numeric("Starting m^2", -4.0, float)
    m_sq_max = prompt_numeric("Ending m^2", 0.5, float)
    if m_sq_min >= m_sq_max:
        print("Note: ending m^2 must be larger than starting m^2. Swapping values.")
        m_sq_min, m_sq_max = m_sq_max, m_sq_min
    return {
        "L": prompt_numeric("Field lattice dimension (L)", 32, int, lambda x: x > 0, "Must be positive."),
        "lambd": prompt_numeric("Quartic coupling (lambda)", 1.0, float, lambda x: x >= 0, "Cannot be negative."),
        "m_sq_min": m_sq_min,
        "m_sq_max": m_sq_max,
        "n_points": prompt_numeric("Number of points in the sweep", 30, int, lambda x: x > 0, "Must be positive."),
        "n_sweeps": prompt_numeric("Sweeps per mass", 10000, int, lambda x: x > 0, "Must be positive."),
        "n_thermal": prompt_numeric("Thermalization sweeps per mass", 2000, int, lambda x: x >= 0, "Cannot be negative."),
        "collect_every": prompt_numeric("Record data every N sweeps", 5, int, lambda x: x > 0, "Must be positive."),
        "step_size": prompt_numeric("Proposal width", 0.6, float, lambda x: x > 0, "Must be positive."),
    }


def gather_sampler_comparison_parameters() -> Dict[str, float | int]:
    print("\nConfiguring the Metropolis vs. Wolff comparison")
    return {
        "L": prompt_numeric("Field lattice dimension (L)", 16, int, lambda x: x > 0, "Must be positive."),
        "m_sq": prompt_numeric("Critical m^2", -3.29, float),
        "lambd": prompt_numeric("Quartic coupling (lambda)", 1.0, float, lambda x: x >= 0, "Cannot be negative."),
        "step_size": prompt_numeric("Proposal width for Metropolis", 0.6, float, lambda x: x > 0, "Must be positive."),
        "n_sweeps": prompt_numeric("Total sweeps", 10000, int, lambda x: x > 0, "Must be positive."),
    }


def run_qho_simulation(params: Dict[str, float | int]) -> None:
    N = int(params["N"])
    path = np.zeros(N)
    data = []
    print("\nRunning the QHO sampler..." )
    for sweep in tqdm(range(int(params["n_sweeps"])), desc="QHO sweeps"):
        local_update(
            path,
            float(params["a"]),
            float(params["m"]),
            float(params["step_size"]),
            pot_type=0,
            lambd=float(params["lambda_poly"]),
        )
        if sweep > int(params["n_thermal"]) and (sweep % int(params["collect_every"]) == 0):
            data.extend(path.copy())
    data = np.array(data)
    if data.size == 0:
        print("No data collected—the sweep count or collect interval might be too small.")
        return
    mean = data.mean()
    std = data.std()
    print(f"Collected {data.size} samples. Mean: {mean:.4f}, Std: {std:.4f}")

    plt.figure(figsize=(10, 6))
    bins = 100
    _, edges, _ = plt.hist(data, bins=bins, density=True, alpha=0.7, label="PIMC samples")
    x_theory = np.linspace(edges[0], edges[-1], 500)
    omega = float(params["omega"])
    m = float(params["m"])
    psi_sq = np.sqrt((m * omega) / np.pi) * np.exp(-m * omega * x_theory**2)
    plt.plot(x_theory, psi_sq, "r--", lw=2, label="Analytical ground state")
    plt.title("Probability Density: QHO")
    plt.xlabel("Position")
    plt.ylabel("Probability density")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def run_double_well_simulation(params: Dict[str, float | int]) -> None:
    N = int(params["N"])
    path = np.zeros(N)
    data = []
    print("\nRunning the Double-Well sampler...")
    for sweep in tqdm(range(int(params["n_sweeps"])), desc="Double-well sweeps"):
        local_update(
            path,
            float(params["a"]),
            float(params["m"]),
            float(params["step_size"]),
            pot_type=1,
            lambd=0.0,
            V0=float(params["V0"]),
            a_dw=float(params["a_param"]),
        )
        if sweep > int(params["n_thermal"]) and sweep % int(params["collect_every"]) == 0:
            data.extend(path.copy())
    data = np.array(data)
    if data.size == 0:
        print("No data collected—the sweep count or collect interval might be too small.")
        return
    print(f"Collected {data.size} samples. Std: {data.std():.4f}")

    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=100, density=True, color="purple", alpha=0.7)
    plt.title("Probability Density: Double-Well Quantum Tunneling")
    plt.xlabel("Position")
    plt.ylabel("Probability density")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def run_phi4_simulation(params: Dict[str, float | int]) -> None:
    L = int(params["L"])
    field = np.zeros((L, L))
    magnetization = []
    print("\nRunning the Phi^4 field sampler...")
    for sweep in tqdm(range(int(params["n_sweeps"])), desc="Phi^4 sweeps"):
        field_local_update(
            field,
            float(params["m_sq"]),
            float(params["lambd"]),
            float(params["step_size"]),
            pot_type=0,
        )
        if sweep > int(params["n_thermal"]) and sweep % int(params["collect_every"]) == 0:
            magnetization.append(np.mean(field))
    if not magnetization:
        print("No magnetization samples collected; try smaller thermalization or smaller collection interval.")
        return
    magnetization = np.array(magnetization)
    print(f"Collected {magnetization.size} magnetization samples. <phi> final: {magnetization[-1]:.4f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    im = axes[0].imshow(field, cmap="RdBu")
    axes[0].set_title(f"Field configuration (m^2={float(params['m_sq']):.2f})")
    fig.colorbar(im, ax=axes[0])
    axes[1].plot(magnetization)
    axes[1].set_title("Order parameter <phi>")
    axes[1].set_xlabel("Sweep")
    axes[1].set_ylabel("Mean field")
    plt.tight_layout()
    plt.show()


def run_sweep_simulation(params: Dict[str, float | int]) -> None:
    L = int(params["L"])
    m_sq_range = np.linspace(float(params["m_sq_min"]), float(params["m_sq_max"]), int(params["n_points"]))
    results = {"mag": [], "chi": []}
    print("\nRunning the susceptibility sweep...")
    for m_sq in m_sq_range:
        field = np.zeros((L, L))
        m_values = []
        desc = f"m^2={m_sq:.2f}"
        for sweep in tqdm(range(int(params["n_sweeps"])), desc=desc, leave=False):
            field_local_update(
                field,
                m_sq,
                float(params["lambd"]),
                float(params["step_size"]),
                pot_type=0,
            )
            if sweep > int(params["n_thermal"]) and sweep % int(params["collect_every"]) == 0:
                m_values.append(np.abs(np.mean(field)))
        if not m_values:
            continue
        m_avg = float(np.mean(m_values))
        chi = (L**2) * (np.mean(np.array(m_values) ** 2) - m_avg**2)
        results["mag"].append(m_avg)
        results["chi"].append(chi)
        print(f"m^2={m_sq:.2f} | <|phi|>={m_avg:.4f} | chi={chi:.4f}")
    if not results["mag"]:
        print("No sweep data collected. Consider lowering thermalization or increasing sweep count.")
        return
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(m_sq_range[: len(results["mag"])], results["mag"], "o-", color="tab:blue", label="Order parameter")
    ax1.set_xlabel("$m^2$")
    ax1.set_ylabel("Magnetization <|phi|>", color="tab:blue")
    ax1.tick_params(axis="y", labelcolor="tab:blue")
    ax2 = ax1.twinx()
    ax2.plot(m_sq_range[: len(results["chi"])], results["chi"], "s--", color="tab:red", label="Susceptibility")
    ax2.set_ylabel("Susceptibility", color="tab:red")
    ax2.tick_params(axis="y", labelcolor="tab:red")
    plt.title("Phi^4 Susceptibility Sweep")
    fig.tight_layout()
    plt.grid(True, alpha=0.3)
    plt.show()


def run_sampler_comparison(params: Dict[str, float | int]) -> None:
    L = int(params["L"])
    mag_metro = []
    mag_wolff = []
    field = np.zeros((L, L))
    print("\nRunning the Metropolis+Wolff comparison...")
    for _ in tqdm(range(int(params["n_sweeps"])), desc="Metropolis sweeps"):
        field_local_update(
            field,
            float(params["m_sq"]),
            float(params["lambd"]),
            float(params["step_size"]),
            pot_type=0,
        )
        mag_metro.append(np.mean(field))
    field = np.zeros((L, L))
    for _ in tqdm(range(int(params["n_sweeps"])), desc="Wolff sweeps"):
        wolff_update(field, float(params["m_sq"]), float(params["lambd"]))
        mag_wolff.append(np.mean(field))
    tau_metro = estimate_tau(mag_metro)
    tau_wolff = estimate_tau(mag_wolff)
    print(f"Estimated tau: Metropolis ~{tau_metro:.1f}, Wolff ~{tau_wolff:.1f}")
    rho_metro = autocorrelation_function(mag_metro)
    rho_wolff = autocorrelation_function(mag_wolff)
    plt.figure(figsize=(10, 5))
    cutoff = min(500, len(rho_metro), len(rho_wolff))
    plt.plot(rho_metro[:cutoff], label=f"Metropolis (tau~{tau_metro:.1f})")
    plt.plot(rho_wolff[:cutoff], label=f"Wolff (tau~{tau_wolff:.1f})")
    plt.axhline(0, color="black", linestyle="--")
    plt.title("Autocorrelation Comparison")
    plt.xlabel("Lag")
    plt.ylabel("Autocorrelation")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


MENU_OPTIONS = {
    "1": {
        "label": "Quantum Harmonic Oscillator",
        "description": "Samples a single-particle path and compares against the analytic ground state.",
        "gather": gather_qho_parameters,
        "runner": run_qho_simulation,
    },
    "2": {
        "label": "Double-Well Quantum Tunneling",
        "description": "Shows bimodal sampling from the double-well path integral.",
        "gather": gather_double_well_parameters,
        "runner": run_double_well_simulation,
    },
    "3": {
        "label": "Phi^4 Field Dynamics",
        "description": "Evolves the 2D Phi^4 field and records the magnetization time series.",
        "gather": gather_phi4_parameters,
        "runner": run_phi4_simulation,
    },
    "4": {
        "label": "Phi^4 Susceptibility Sweep",
        "description": "Sweeps m^2 to find the susceptibility spike that signals symmetry breaking.",
        "gather": gather_sweep_parameters,
        "runner": run_sweep_simulation,
    },
    "5": {
        "label": "Metropolis vs. Wolff",
        "description": "Compares autocorrelation decay for Metropolis and Wolff cluster moves.",
        "gather": gather_sampler_comparison_parameters,
        "runner": run_sampler_comparison,
    },
}


def display_menu() -> None:
    print("\nWhat would you like to do?")
    for key, spec in MENU_OPTIONS.items():
        print(f"  {key}. {spec['label']} - {spec['description']}")
    print("  q. Exit")


def launch_interface() -> None:
    print(WELCOME_TEXT)
    while True:
        try:
            display_menu()
            choice = input("Enter the number of the scenario you want to run: ").strip().lower()
            if choice in ("q", "quit", "exit"):
                print("Thanks for exploring the PIMC suite. Goodbye!")
                break
            spec = MENU_OPTIONS.get(choice)
            if not spec:
                print("Unknown choice. Please select a number from the menu.")
                continue
            params = spec["gather"]()
            spec["runner"](params)
        except KeyboardInterrupt:
            print("\nInterrupted. Exiting the interface.")
            break


if __name__ == "__main__":
    launch_interface()
