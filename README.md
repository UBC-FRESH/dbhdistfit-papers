# dbhdistfit-papers

Repository for two Forest Science Brief Communication manuscripts on diameter-distribution
fitting:

- `dbhdistfit-hps` — harvest planning study (submitted to *Forest Science*, Brief
  Communication, 2024).
- `dbhdistfit-truncdata` — truncated-diameter follow-up (in progress for the same venue).

Historical notebooks and previous project scaffolds now live under `legacy/` to keep the
active manuscripts streamlined.

## Quick Start

```bash
git clone https://github.com/UBC-FRESH/dbhdistfit-papers.git
# HPS manuscript workflow
cd dbhdistfit-papers/dbhdistfit-hps
make env          # create virtual environment (Python 3.12+)
make data         # preprocess PSP tallies from the legacy pickle
make figures      # regenerate comparison plots
make tables       # regenerate comparison tables
make manuscript   # compile LaTeX sources

# Truncated-data manuscript workflow
cd ../dbhdistfit-truncdata
make repro        # optional: run full pipeline (data + tables + figures + notebook)
```

All generated artefacts are placed under `figures/`, `tables/`, and `manuscript/build/`.
The `make repro` target executes the full pipeline, including the reproducibility
notebook in `notebooks/`.

## Data Sources

- `legacy/pspdistfit/dat/misc/tiges_final_full.p` — legacy Quebec PSP stem tallies underpinning
  the truncated analysis. The preprocessing script documents the BlockManager patch used
  to load the pickle under pandas 2.x. Set the environment variable
  `DBHDISTFIT_TRUNCDATA_PICKLE` to point to an alternative copy if needed.
- `dbhdistfit-hps/data.local/` — optional DataLad dataset with the harmonised HPS inputs
  used for the companion study. Run `datalad get` to retrieve the files when working
  inside that subproject.

The refreshed pipeline (`scripts/preprocess_data.py`) bins the legacy PSP tallies into
2 cm classes (10–60 cm DBH) and reproduces the stand tables shipped with the original
article. It retains unit non-linear least-squares weights for parity with the published
baseline; per-bin inverse-variance weighting is illustrated in the companion notebook.

## Companion Notebook

`legacy/pspdistfit/dbhdistfit_method-truncdata.ipynb` walks through the end-to-end analysis:
loading the legacy pickle, applying the BlockManager patch, binning tallies, fitting the
Weibull/Gamma families, and comparing truncated versus two-stage fits. The notebook is
referenced in the manuscript as the primary reproducibility artefact instead of separate
supplementary information.

To execute the notebook:

```bash
cd dbhdistfit-papers
source .venv/bin/activate        # or use the project environment
jupyter nbconvert --to notebook --execute \
  legacy/pspdistfit/dbhdistfit_method-truncdata.ipynb \
  --output dbhdistfit_method-truncdata.executed.ipynb
```

## Repository Structure

```
dbhdistfit-hps/         # harvest-planning manuscript (submitted)
dbhdistfit-truncdata/   # truncated-diameter manuscript (in preparation)
legacy/                 # archived notebooks, original PSP analysis, prior scaffolds
tables/                 # (legacy) combined tables retained for reference
tmp/                    # scratch space used during builds
```

## Contact

For questions or data access issues, open a GitHub issue or reach out to the FRESH Lab
team at UBC Forestry.
