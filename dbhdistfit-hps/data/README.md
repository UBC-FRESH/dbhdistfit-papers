# Data Directory

Place processed datasets required by the reproducibility pipeline here.

Required artefact:

- `processed/binned_meta_plots.parquet` — binned stand-level tallies with
  columns `species_group`, `cover_type`, `dbh_cm`, `tally`, and optionally
  `expansion_factor`.

Optional artefacts:

- `raw/` — original PSP extracts or HPS tallies (not tracked in version control).
- `interim/` — intermediate files produced during preprocessing.
