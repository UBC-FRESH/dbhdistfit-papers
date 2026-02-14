# dbhdistfit-truncdata

Reimplementation of the truncated-diameter fitting manuscript using the modern reproducible project scaffold. The scope mirrors the legacy `dbhdistfit-old/dbhdistfit_method-truncdata` article while adopting the automated workflow used for the HPS paper.

## Pipeline Overview
- `make data` bins the legacy Quebec PSP pickle (`pspdistfit/dat/misc/tiges_final_full.p`)
  into 2 cm classes, reproducing the published stand tables via
  `scripts/preprocess_data.py`. Set `DBHDISTFIT_TRUNCDATA_PICKLE` to override the source.
- `make tables` / `make figures` regenerate the comparison artefacts via
  `scripts/generate_tables.py` and `scripts/generate_figures.py`.
- `make manuscript` builds the LaTeX sources under `manuscript/`; title page, cover
  letter, EM package, and preprint targets mirror the HPS project.
- Reproducibility notebooks live in `notebooks/`; `pspdistfit/dbhdistfit_method-truncdata.ipynb`
  provides an annotated walkthrough that the manuscript cites in lieu of standalone SI.

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

## Notes on Bin Weights

The default pipeline fits the Weibull and Gamma families with unit bin weights to enable
a direct comparison with the truncated-density baseline from the legacy article. The
companion notebook illustrates how to construct inverse-variance weights from per-plot
tallies for analysts who wish to emphasise dense interior bins and down-weight sparse
tails.
