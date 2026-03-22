# qlab

This repository is organized as three independent quantum computing subprojects.

## Subprojects

### `bloch-spheres-animations`
A visualization project that generates MP4 animations of single-qubit state evolution on the Bloch sphere from multiple camera views. It includes gate demos (Pauli, phase, rotations) and state-preparation examples.

### `grover`
A notebook-driven project focused on Grover search ideas, currently centered on a subset-sum experiment in `grover/notebooks/grover-subset-sum.ipynb`.

### `qubo-degeneracy-analysis`
A QUBO analysis project with utilities and solver code (`src/qubo.py`, `src/solver.py`, `src/utils.py`) plus a QAOA exploration notebook (`notebooks/qaoa-experiment.ipynb`).

## Setup and run: `bloch-spheres-animations`

1. Create and activate a virtual environment.
2. Install dependencies.
3. Create `bloch-spheres-animations/.env` with required paths.
4. Run the animation script.

```bash
cd <your-path>/qlab/bloch-spheres-animations
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

Create `.env` in `bloch-spheres-animations`:

```dotenv
BLOCH_FFMPEG_PATH=<your-path>/bin/ffmpeg
BLOCH_OUTPUT_VIDEOS_PATH=<your-path>/qlab/bloch-spheres-animations/videos/bloch_spheres
```

Run:

```bash
cd <your-path>/qlab/bloch-spheres-animations
python src/bloch_spheres_main.py
```

Notes:
- `BLOCH_FFMPEG_PATH` and `BLOCH_OUTPUT_VIDEOS_PATH` are required; the program exits if either is missing.
- Output videos are written to `BLOCH_OUTPUT_VIDEOS_PATH`.
- If needed on macOS, install ffmpeg with `brew install ffmpeg`.

