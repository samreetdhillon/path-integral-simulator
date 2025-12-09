## The Physical Picture: Quantum Mechanics on a Grid

This project is simulating the behavior of a quantum particle or a quantum field in a one-dimensional system. The core idea is to translate the complex rules of quantum mechanics into something a computer can handle using a technique called the **Path Integral Formulation**.

### Quantum to Classical Mapping (Path Integral)

- **The Problem**: In quantum mechanics, a particle doesn't follow a single path; it takes all possible paths between two points. This is incredibly complex.
- **The Solution (Feynman's Path Integral)**: This simulator "solves" this by mapping the quantum particle's behavior in time to the behavior of a classical ring of connected beads (the "path") on a potential energy surface.
  - **The Path**: The path variable (an array of numbers) represents a path in imaginary time. You can think of it as a chain of $N$ beads (where $N$ is path_len or N in your code) linked together. Each bead's position, $x_i$, is the particle's location at a specific point in imaginary time.
  - **The Connection to Energy** : The probability of a specific path is related to a value called the Euclidean Action (your action function). The smaller the action, the more likely the path.
    - **Kinetic Term**: The $(x_{i+1} - x_i)^2$ part penalizes paths that are too "wiggly" (large, rapid changes in position), similar to how kinetic energy works.
    - **Potential Term**: The $V(x_i)$ part penalizes paths that spend too much time in high-energy regions.

### The Physical Systems We Are Simulating

The project implements two main systems by changing the potential energy function $V(x)$:

- **Harmonic Oscillator (V_harmonic)**: This is like a tiny, ideal spring. The potential energy is $V(x) \propto x^2$. The particle is pulled toward the center ($x=0$) and has smooth, predictable quantum behavior.
- **Double-Well Potential (V_double_well) / Phi-4 Theory (V_phi4)**: This is a crucial physical system, often leading to phase transitions. The potential looks like an "M" or a camel's back (two minima separated by a hump).
  - For the quantum particle, the system has two preferred ground states (the two wells). The particle can "tunnel" between them.
  - In the $\phi^4$ theory, the parameter $\lambda$ controls the shape of the potential. Changing $\lambda$ simulates a change in the physical system, potentially moving it from a single-well (like the harmonic oscillator) to a double-well. This is a common way to simulate a phase transition (like water turning to ice).

## The Method: Monte Carlo Simulation

Since checking all possible paths is impossible, we use a clever statistical trick called **Monte Carlo**.

- **The Goal**: Find the most probable paths (those with the lowest action) to accurately calculate physical properties.
- **The Tool (Metropolis Algorithm)**: The `metropolis_update` and `metropolis_sweep` functions implement the Metropolis algorithm.
  1. **Select a Bead**: Randomly pick one bead ($x_i$) on the path.
  2. **Propose a Change**: Propose a small, random shift to its position ($\phi_{new} = \phi_{old} + \text{random\_step}$).
  3. **Calculate Cost Change**: Calculate the change in the system's action, $\Delta S$, using `local_action_diff`. This is fast because only the change around the moved bead matters.
  4. **Accept or Reject:**
     - If the change lowers the action ($\Delta S < 0$), the new position is always accepted (it's a better, more probable path).
     - If the change raises the action ($\Delta S > 0$), it is accepted with a probability $\propto e^{-\Delta S}$. This is the genius of the method: it allows the system to sometimes move to higher-action states, which is essential to avoid getting stuck and to properly explore all important paths.
- **Thermalization (`n_therm`)**: The initial `path` is usually a guess (e.g., all zeros). The thermalization sweeps run the Metropolis algorithm to let the path settle down into a representative low-action state.

## The Results: Measuring Physical Properties

Once the system has thermalized, we collect "snapshots" of the path and calculate **observables**—the actual physical properties of the system.

- $\langle \phi^2 \rangle$ and $\langle \phi^4 \rangle$:These are measurements of the average square and fourth power of the field value $\phi$ (the particle's position). They are the fundamental building blocks for other measurements.
- **Susceptibility ($\chi$)**: Our `susceptibility` function measures how much the system's average field value "wants" to change if an external force were applied. It often spikes at a phase transition.
- **Binder Cumulant ($U_4$)**: This quantity is specifically designed to locate a critical point (the exact spot of a phase transition). Its value depends on the shape of the $\phi$ histogram.
- **Two-Point Correlator ($G(r)$)**: This measures how correlated the field value at one point in imaginary time ($\phi_i$) is with the field value at another point ($\phi_{i+r}$). In simpler terms, it measures how long-range the interactions are.
- **Effective Mass ($m_{eff}$)**: This is calculated from the correlator and represents the mass of the quantum particle/excitation in the system. A smaller mass means the influence of the particle spreads further and the system is more correlated.

In short, we are using a statistical sampling method (Monte Carlo) to study the fundamental rules of quantum physics, specifically looking for changes in the system's behavior (like a phase transition) as we vary the potential's shape (the $\lambda$ parameter).
