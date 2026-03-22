from qutip import Bloch, basis, sigmax, sigmay, sigmaz, Qobj
from scipy.linalg import expm
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import os

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",   # Computer Modern (LaTeX-like)
    "mathtext.rm": "serif",
})

# ------------------------------------------------------------
# Rotation gates
# ------------------------------------------------------------
def rx(theta):
    return Qobj(expm(-1j * theta/2 * sigmax().full()))

def ry(theta):
    return Qobj(expm(-1j * theta/2 * sigmay().full()))

def rz(theta):
    return Qobj(expm(-1j * theta/2 * sigmaz().full()))

# ------------------------------------------------------------
# Hadamard via rotations
# ------------------------------------------------------------
def hadamard(t):
    if t <= 0.5:
        return rx(2 * np.pi * t)
    else:
        return ry(np.pi * (t - 0.5)) @ rx(np.pi)

# ------------------------------------------------------------
# Complex → LaTeX helper
# ------------------------------------------------------------
def complex_to_latex(z, tol=1e-3):
    r, i = np.real(z), np.imag(z)
    r = 0 if abs(r) < tol else r
    i = 0 if abs(i) < tol else i

    if i == 0:
        return f"{r:.2f}"
    if r == 0:
        return f"{i:.2f}i"
    sign = "+" if i > 0 else "-"
    return f"({r:.2f} {sign} {abs(i):.2f}i)"

# ------------------------------------------------------------
# Main animation function
# ------------------------------------------------------------
def animate_gate_4_quadrants(
    state,
    gate_func,
    gate_name,
    n_frames=100,
    save_path="bloch_gate.mp4",
    phase_gate=False
):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    ts = np.linspace(0, 1, n_frames)

    fig = plt.figure(figsize=(12, 12))

    quadrants = [
        ((2,2,1), dict(elev=30, azim=45),  "3D overview"),
        ((2,2,2), dict(elev=90, azim=0), "Z view  (|0⟩, |1⟩)"),
        ((2,2,3), dict(elev=0, azim=90), "X view  (|+⟩, |−⟩)"),
        ((2,2,4), dict(elev=0, azim=0), "Y view  (|+i⟩, |−i⟩)"),
    ]

    axes, blochs = [], []

    for pos, cam, title in quadrants:
        ax = fig.add_subplot(*pos, projection="3d")
        ax.view_init(**cam)

        b = Bloch(axes=ax)
        lpos = 1.1
        b.xlabel = [r"$\left|+\right\rangle$", r"$\left|-\right\rangle$"]
        b.ylabel = [r"$\left|+\!i\right\rangle$", r"$\left|-\!i\right\rangle$"]
        b.zlabel = [r"$\left|0\right\rangle$", r"$\left|1\right\rangle$"]
        b.xlpos = [lpos, -lpos]
        b.ylpos = [lpos, -lpos]
        b.zlpos = [lpos, -lpos]
        b.font_size = 14

        bbox = ax.get_position()
        x_center = bbox.x0 + bbox.width / 2
        y_top = bbox.y1 + 0.02  # adjust padding if needed

        fig.text(
            x_center, y_top, title,
            ha="center", va="bottom",
            fontsize=15,
            fontweight="bold",
        )

        # ax.set_title(title[0])
        # print(ax.title.get_position(), ax.title.get_visible())

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        axes.append(ax)
        blochs.append(b)

    # Inner quadrant cross (not touching borders)
    # fig.add_artist(plt.Line2D(
    #     [0.5, 0.5], [0.18, 0.88],
    #     transform=fig.transFigure, lw=2, color="black"
    # ))
    # fig.add_artist(plt.Line2D(
    #     [0.08, 0.92], [0.53, 0.53],
    #     transform=fig.transFigure, lw=2, color="black"
    # ))

    # Main title
    fig.suptitle(
        gate_name,
        fontsize=22,
        color="red",
        fontweight="bold",
        y=0.96
    )

    # Dirac notation overlay
    dirac_text = fig.text(
        0.5, 0.06,
        "",
        ha="center",
        fontsize=18
    )

    base_views = [q[1] for q in quadrants]

    def update(i):
        t = ts[i]
        U = gate_func(t)
        psi = U @ state

        for b in blochs:
            b.clear()
            b.add_states(psi)
            b.make_sphere()

        if phase_gate:
            for ax, base in zip(axes, base_views):
                ax.view_init(
                    elev=base["elev"],
                    azim=base["azim"] + 360 * t
                )

        # Always show raw coefficients
        α = psi.full()[0,0]
        β = psi.full()[1,0]
        α_str = complex_to_latex(α)
        β_str = complex_to_latex(β)
        terms = [f"{α_str}\\,|0\\rangle"]
        sign = " + " if not β_str.startswith("-") else " "
        terms.append(f"{sign}{β_str}\\,|1\\rangle")
        state_line = rf"$|\psi\rangle = {' '.join(terms)}$"
        coeff_line = rf"$\alpha = {α_str}, \quad \beta = {β_str}$"
        dirac_text.set_text(state_line + "\n" + coeff_line)
        return []

    ani = animation.FuncAnimation(
        fig, update, frames=n_frames, blit=False
    )

    ani.save(save_path, writer="ffmpeg", fps=20, dpi=150)
    plt.close(fig)
    print(f"Saved: {save_path}")
