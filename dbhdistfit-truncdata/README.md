# dbhdistfit-truncdata

Reimplementation of the truncated-diameter fitting manuscript using the modern reproducible project scaffold. The scope mirrors the legacy `dbhdistfit-old/dbhdistfit_method-truncdata` article while adopting the automated workflow used for the HPS paper.

## Planned Components
- Reusable data-processing pipeline that ingests fixed-area PSP tallies (shared raw source with the HPS project) and applies constant plot expansion factors instead of HPS-only logic.
- Scripted generation of all tables and figures comparing the two-stage estimator with classical truncated-distribution fits.
- Modular LaTeX manuscript (`manuscript/`) aligned with Forest Science formatting patterns used previously, including automated word-count, EM packaging, and EarthArXiv preprint builds.
- Jupyter notebook(s) that demonstrate the analysis end-to-end for transparency and reviewer supplement needs.

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

## Next Steps
1. Port mathematical exposition and experimental design from the legacy LaTeX into sectioned files.
2. Stand up preprocessing scripts that reuse the PSP dataset while respecting fixed-area expansions.
3. Rebuild tables/figures as code-generated artefacts and wire them into the manuscript.
4. Finalise submission tooling (double-blind package, checklists, EarthArXiv cover page).
