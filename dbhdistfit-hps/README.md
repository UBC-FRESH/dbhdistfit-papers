# dbhdistfit-hps

Fully reproducible project scaffold for the revised manuscript on diameter
distribution fitting with horizontal point sampling (HPS) data.

## Layout

- `manuscript/` — LaTeX source, bibliography, journal submission assets.
- `notebooks/` — reproducible exploration notebooks (rendered via Makefile).
- `scripts/` — pure-Python data processing, fitting, figure/table generation.
- `data/` — managed input datasets (raw + derived), tracked via `.gitignore`.
- `figures/` — auto-generated manuscript figures.
- `tables/` — auto-generated manuscript tables.

## Make Targets

Run `make help` for the list of supported workflows. Core targets include:

- `make figures` — run scripted figure generation into `figures/`.
- `make tables` — run scripted table generation into `tables/`.
- `make manuscript` — compile the LaTeX manuscript.
- `make repro` — orchestrate a full reproducibility pass (data → outputs).

## Environment

The project expects a modern Python 3.11+ environment. Rebuild reproducible
artefacts using `environment.yml` (conda/mamba) or `requirements.txt` (pip).
To create a local virtual environment with the standard library tools, run:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
