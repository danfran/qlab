import numpy as np
import os
from pathlib import Path
from qutip import basis, Qobj
from scipy.linalg import expm, logm
from dotenv import load_dotenv

from bloch_spheres import rx, ry, rz, hadamard, animate_gate_4_quadrants


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")


def get_required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None or not value.strip():
        raise SystemExit(
            f"Missing required environment variable '{var_name}' in {ROOT_DIR / '.env'}"
        )
    return value


def make_videos(output_videos_dir: str | Path):
    # Precompute for Hadamard interpolation
    H = Qobj([[1,1],[1,-1]]) / np.sqrt(2)
    logH = logm(H.full())

    cases = [
        # Basis
        (basis(2, 0), lambda t: Qobj(np.eye(2)), "Basis |0>", False),
        (basis(2, 1), lambda t: Qobj(np.eye(2)), "Basis |1>", False),

        # Hadamard / X-basis
        (basis(2, 0), lambda t: rz(np.pi / 2 * t) @ ry(np.pi / 2 * t) @ rz(np.pi / 2 * t), "Hadamard |0> → |+>", False),
        (basis(2, 1), lambda t: rz(np.pi / 2 * t) @ ry(np.pi / 2 * t) @ rz(np.pi / 2 * t), "Hadamard |1> → |->", False),

        # Y-basis
        (basis(2, 0), lambda t: ry(np.pi / 2 * t), "Ry(π/2) → |+>", False),
        (basis(2, 0), lambda t: ry(-np.pi / 2 * t), "Ry(-π/2) → |->", False),

        # Pauli
        (basis(2, 0), lambda t: rx(np.pi * t), "Pauli-X", False),
        (basis(2, 0), lambda t: ry(np.pi * t), "Pauli-Y", False),
        ((basis(2, 0) + basis(2, 1)).unit(), lambda t: rz(np.pi * t), "Pauli-Z", True),

        # Phase
        (basis(2, 0), lambda t: rz(np.pi / 2 * t), "S gate", True),
        (basis(2, 0), lambda t: rz(np.pi / 4 * t), "T gate", True),

        # Rotations
        (basis(2, 0), lambda t: rx(np.pi / 2 * t), "Rx(π/2)", False),
        (basis(2, 0), lambda t: rx(np.pi * t), "Rx(π)", False),
        (basis(2, 0), lambda t: ry(np.pi / 2 * t), "Ry(π/2)", False),
        (basis(2, 0), lambda t: ry(np.pi * t), "Ry(π)", False),

        # Z-rotations on |+>
        ((basis(2, 0) + basis(2, 1)).unit(), lambda t: rz(np.pi / 2 * t), "Rz(π/2) on |+>", True),
        ((basis(2, 0) + basis(2, 1)).unit(), lambda t: rz(np.pi * t), "Rz(π) on |+>", True),

        # Arbitrary states
        (basis(2, 0),
         lambda t: rz(np.pi / 3 * t) @ ry(2 * np.arccos(np.sqrt(0.3)) * t),
         "Prepare α|0> + β|1>",
         True),

        (basis(2, 0),
         lambda t: rz(np.pi / 2 * t) @ ry(np.pi / 2 * t),
         "Prepare |0> + i|1>",
         True),
    ]

    output_videos_dir = Path(output_videos_dir)

    for i, (psi0, gate, title, phase) in enumerate(cases):
        try:
            final_op = gate(1.0)
            final_state = final_op * psi0
            print(f"Case {i}: {title}")
            print(f"Initial state: {psi0}")
            print(f"Final operator: {final_op}")
            print(f"Final state: {final_state}")
            print("---")
            animate_gate_4_quadrants(
                psi0,
                gate,
                title,
                # save_path=f"videos/bloch_spheres/{i:02d}_{title.replace(' ', '_')}.mp4",
                save_path=str(output_videos_dir / f"{i:02d}.mp4"),
                phase_gate=phase
            )
        except Exception as e:
            print(f"Error in case {i}: {e}")
            continue


if __name__ == "__main__":
    # verify that ffmpeg is visible
    import matplotlib as mpl
    ffmpeg_path = get_required_env("BLOCH_FFMPEG_PATH")
    output_videos_dir = get_required_env("BLOCH_OUTPUT_VIDEOS_PATH")

    mpl.rcParams['animation.ffmpeg_path'] = ffmpeg_path
    print(mpl.animation.writers.list())
    print(f"Using ffmpeg path: {ffmpeg_path}")
    print(f"Using output path: {output_videos_dir}")

    make_videos(output_videos_dir)
