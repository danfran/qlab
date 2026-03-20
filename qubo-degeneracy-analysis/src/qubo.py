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

weights = [
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
]

subset = [1,3,3,5]

target = 8

def build_subset_sum_qubo(
    weights: list[list[int]],
    subset: list[int],
    target: int,
) -> list[tuple[str, list[int], float]]:
    """Convert the subset to Pauli list.
    """
    n = len(subset)
    pauli_list = []

    for i in range(0, n):
        for j in range(i + 1, n):
            weight = 2 * subset[i] * subset[j]
            pauli_list.append(("ZZ", [i, j], weight))

    for i in range(n):
        coeff = subset[i] ** 2 - 2 * target * subset[i]
        pauli_list.append(("Z", [i], coeff))

    return pauli_list


subset_sum_qubo = build_subset_sum_qubo(weights, subset, target)
print(subset_sum_qubo)
cost_hamiltonian = SparsePauliOp.from_sparse_list(subset_sum_qubo, len(subset))
print("Cost Function Hamiltonian:", cost_hamiltonian)