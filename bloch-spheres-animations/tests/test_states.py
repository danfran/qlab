import numpy as np
from qutip import basis, Qobj
from bloch_spheres import rx, ry, rz, complex_to_latex

def test_hadamard_states():
    # Initial state |0>
    psi0 = basis(2, 0)

    # Gate function for Hadamard decomposition
    def gate(t):
        return rz(np.pi / 2 * t) @ ry(np.pi / 2 * t) @ rz(np.pi / 2 * t)

    # Expected values at test points
    expected_values = {
        0.0: (1+0j, 0j),
        0.5: (0.6532814824381883-0.6532814824381883j, 0.38268343236508984+0j),
        1.0: (1.1102230246251565e-16-0.7071067811865476j, 0.7071067811865476+0j)
    }

    for t, (expected_α, expected_β) in expected_values.items():
        U = gate(t)
        psi = U @ psi0
        α = psi.full()[0, 0]
        β = psi.full()[1, 0]

        assert np.allclose(α, expected_α), f"At t={t}, α mismatch: got {α}, expected {expected_α}"
        assert np.allclose(β, expected_β), f"At t={t}, β mismatch: got {β}, expected {expected_β}"

    # Test Dirac display logic at t=0 (only |0>)
    t = 0.0
    U = gate(t)
    psi = U @ psi0
    α = psi.full()[0, 0]
    β = psi.full()[1, 0]

    terms = []
    tol = 1e-3
    if abs(α) > tol:
        terms.append(f"{complex_to_latex(α)}\\,|0\\rangle")
    if abs(β) > tol:
        coeff_str = complex_to_latex(β)
        if terms:
            sign = " + " if not coeff_str.startswith("-") else " "
            terms.append(f"{sign}{coeff_str}\\,|1\\rangle")
        else:
            terms.append(f"{coeff_str}\\,|1\\rangle")
    dirac = f"$|\\psi\\rangle = {' '.join(terms)}$"

    # Check that the final operator is not the standard Hadamard
    U_final = gate(1.0)
    H = Qobj([[1,1],[1,-1]]) / np.sqrt(2)
    assert not np.allclose(U_final.full(), H.full()), "Decomposition unexpectedly matches standard Hadamard"
