# dbhdistfit-truncdata

Reimplementation of the truncated-diameter fitting manuscript using the modern reproducible project scaffold. The scope mirrors the legacy `dbhdistfit-old/dbhdistfit_method-truncdata` article while adopting the automated workflow used for the HPS paper.

## Pipeline Overview
- `make data` expands fixed-area PSP tallies (shared with the HPS project) and produces normalised stand tables in `data/processed/`.
- `make tables` / `make figures` regenerate the comparison artefacts via `scripts/generate_tables.py` and `scripts/generate_figures.py`.
- `make manuscript` builds the LaTeX sources under `manuscript/`; title page, cover letter, EM package, and preprint targets mirror the HPS project.
- A reproducibility notebook (`notebooks/dbhdistfit_truncdata.ipynb`) executes the end-to-end pipeline for reviewer supplements.

## Directory Layout
```
config/                # YAML configuration for script orchestration
scripts/               # Python modules for preprocessing, fitting, tables, figures
manuscript/            # LaTeX sources (main.tex + section files)
figures/, tables/      # Script outputs kept under version control
notebooks/             # Executable reproducibility notebooks
data/                  # DataLad subdataset (to be initialised) for PSP fixed-area inputs
preprint/, em-submission/, tmp/  # Build artefacts
```

## Remaining Tasks
1. Finalise the manuscript narrative while keeping the brief word limit satisfied.
2. Expand the data availability statement with DataLad usage notes and provenance for the PSP inputs.
3. Finalise citation updates and polish the title page / cover letter ahead of submission.
