## Submission Readiness Checklist (Draft)

| Category | Status | Notes |
| --- | --- | --- |
| Article scope | ⚠️ In Progress | Narrative refresh nearly complete; target journal confirmation outstanding. |
| Data pipeline | ✅ Ready | Fixed-area preprocessing rebuilt around legacy PSP pickle (`scripts/preprocess_data.py`). |
| Figures & tables | ✅ Ready | Regenerated after data refresh via `scripts/generate_figures.py` / `generate_tables.py`. |
| Manuscript formatting | ✅ Ready | Word limit (<2,000 incl. refs) and 150-word abstract confirmed; build regenerates cleanly via `make dbhdistfit-truncdata-repro`. |
| Word count block | ✅ Ready | Automated via `manuscript/scripts/wordcount.sh` and populated in `main.tex`. |
| Statements & Declarations | ✅ Ready | Funding, employment, and data statements updated in `main.tex`. |
| Data availability | ✅ Ready | Manuscript cites GitHub repo; README/DataLad guidance and notebook references refreshed. |
| Double-blind package | ✅ Ready | `make em-submission` verified; flat archive produced. |
| Preprint | ✅ Ready | `make preprint` generates EarthArXiv cover + manuscript bundle. |
| Cover letter | ⚠️ In Progress | Forest Science template drafted; final date/signature to insert prior to submission. |
| ORCID & metadata | ✅ Ready | ORCID recorded on title page; submission metadata summarised in `submission-metadata.md`. |
| Final proofing | ⚠️ Pending | Word count, linting, and QA to run at finalisation. |

### Immediate Next Steps
1. Complete Forest Science style audit adjustments (front matter wording, title-page checks, reference format).
2. Finalise cover letter (insert submission date, add any co-author signatures if required).
3. Schedule final proofing pass (spellcheck, linting, repository clean build) prior to portal upload.
