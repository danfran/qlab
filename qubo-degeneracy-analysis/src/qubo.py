import rustworkx as rx
from rustworkx.visualization import mpl_draw as draw_graph
import numpy as np
from scipy.optimize import minimize
from collections import defaultdict
from typing import Sequence


from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import QAOAAnsatz
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# from qiskit_ibm_runtime import QiskitRuntimeService
# from qiskit_ibm_runtime import Session, EstimatorV2 as Estimator
# from qiskit_ibm_runtime import SamplerV2 as Sampler

# weights = [
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
#     [1.0, 1.0, 1.0, 1.0],
# ]


from itertools import product



subset = [1,3,3,5]

target = 8

def build_subset_sum_qubo(
    subset: list[int],
    target: int,
) -> list[tuple[str, list[int], float]]:
    """Convert the subset to Pauli list.
    """
    n = len(subset)
    pauli_list = []

    for i in range(n):
        for j in range(i + 1, n):
            weight = 2 * subset[i] * subset[j]
            pauli_list.append(("ZZ", [i, j], weight))

    for i in range(n):
        coeff = subset[i] ** 2 - 2 * target * subset[i]
        pauli_list.append(("Z", [i], coeff))

    return pauli_list


def build_ising_parameters(subset, target):
    n = len(subset)

    h = [0.0] * n
    J = [[0.0]*n for _ in range(n)]

    # Linear terms
    for i in range(n):
        h[i] = 0.5 * subset[i]**2 - target * subset[i]

    # Interaction terms
    for i in range(n):
        for j in range(i + 1, n):
            J[i][j] = 0.5 * subset[i] * subset[j]

    return h, J

def ising_energy(z, h, J):
    n = len(z)
    energy = 0

    # linear terms
    for i in range(n):
        energy += h[i] * z[i]

    # interaction terms
    for i in range(n):
        for j in range(i + 1, n):
            energy += J[i][j] * z[i] * z[j]

    return energy

def all_spin_configs(n):
    return list(product([-1, 1], repeat=n))

def z_to_x(z):
    return [(1 - zi) // 2 for zi in z]


# brute force check
h, J = build_ising_parameters(subset, target)

n = len(subset)

configs = all_spin_configs(n)

results = []

for z in configs:
    x = z_to_x(z)

    e_true = (sum(w * xi for w, xi in zip(subset, x)) - target) ** 2
    e_ising = ising_energy(z, h, J)

    results.append((z, x, e_true, e_ising))

# sort by true energy
results.sort(key=lambda t: t[2])

for r in results:
    print(r)




subset_sum_qubo = build_subset_sum_qubo(subset, target)
print(subset_sum_qubo)
cost_hamiltonian = SparsePauliOp.from_sparse_list(subset_sum_qubo, len(subset))
print("Cost Function Hamiltonian:", cost_hamiltonian)