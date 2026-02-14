# Forest Science Submission Metadata (R1)

| Field | Value |
| --- | --- |
| Journal | *Forest Science* |
| Article type | Brief Communication |
| Manuscript title | *A Two-Stage Fitting Method for Truncated Stem Diameter Distributions* |
| Corresponding author | Gregory E. Paradis (`gregory.paradis@ubc.ca`) |
| ORCID | 0000-0001-9618-8797 |
| Affiliation | Department of Forest Resources Management, University of British Columbia, Vancouver, Canada |
| Word count (incl. references) | TBD (update after revisions) |
| Word count (excl. references) | TBD (update after revisions) |
| Abstract word count | TBD |
| Supplementary information | None (materials hosted in companion repository) |
| Figures | 1 (verify after edits) |
| Tables | 1 (verify after edits) |
| Data & code | https://github.com/UBC-FRESH/dbhdistfit-papers (branch `feature/dbhdistfit-truncdata-r1`) |
| Repository DOI | To be assigned if requested by journal |
| Cover letter contact | Gregory E. Paradis (`gregory.paradis@ubc.ca`) |
| Revision due date | 15 Feb 2026 |

## Notes

- Primary workflow is in `dbhdistfit-truncdata/` with r1 source under `manuscript-r1/`.
- Local PSP pickle is stored at `dbhdistfit-truncdata/data/interim/tiges_final_full.p` and used by default in `make data`.
- Reproducibility workflow uses `make repro` and the notebook `dbhdistfit-truncdata/notebooks/dbhdistfit_truncdata.ipynb`.
- Declarations are embedded in `dbhdistfit-truncdata/manuscript-r1/main.tex` (Statements and Declarations section).
