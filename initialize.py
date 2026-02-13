import os

def create_structure():
    structure = [
        "core",              # Core physics engines (Metropolis, Actions)
        "core/samplers",     # Sampling algorithms (Metropolis, Wolff)
        "core/potentials",   # V(x) definitions and Field Actions
        "experiments",       # Scripts for specific runs (QHO, Phi4)
        "notebooks",         # Data analysis and plotting
        "data/raw",          # Raw Markov Chain trajectories
        "data/processed",    # Calculated observables
        "tests"              # Unit tests for discretization/energy
    ]

    files = {
        "requirements.txt": "numpy\nmatplotlib\nscipy\ntqdm\nnumba",
        "README.md": "# PIMC Scalar Field Theory\nSimulation of QFT on a lattice.",
        "core/__init__.py": "",
        "core/samplers/metropolis.py": "# Metropolis-Hastings logic",
        "experiments/run_qho.py": "# Main script for Harmonic Oscillator",
        "experiments/run_phi4.py": "# Main script for Phi^4 theory",
        ".gitignore": "data/\n__pycache__/\n*.npy"
    }

    # Create directories
    for folder in structure:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {folder}")

    # Create initial files
    for filepath, content in files.items():
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Created file: {filepath}")

if __name__ == "__main__":
    create_structure()
    print("\nProject structure initialized successfully.")