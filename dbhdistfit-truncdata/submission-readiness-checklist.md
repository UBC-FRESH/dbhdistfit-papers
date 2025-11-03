## Submission Readiness Checklist (Draft)

| Category | Status | Notes |
| --- | --- | --- |
| Article scope | ✅ Ready | Forest Science Brief Communication scope confirmed; narrative aligned with word/figure limits. |
| Data pipeline | ✅ Ready | Fixed-area preprocessing rebuilt around legacy PSP pickle (`scripts/preprocess_data.py`). |
| Figures & tables | ✅ Ready | Regenerated after data refresh via `scripts/generate_figures.py` / `generate_tables.py`. |
| Manuscript formatting | ✅ Ready | Word limit (<2,000 incl. refs) and 150-word abstract confirmed; build regenerates cleanly via `make dbhdistfit-truncdata-repro`. |
| Word count block | ✅ Ready | Automated via `manuscript/scripts/wordcount.sh` and populated in `main.tex`. |
| Statements & Declarations | ✅ Ready | Funding, employment, and data statements updated in `main.tex`. |
| Data availability | ✅ Ready | Manuscript cites GitHub repo; README/DataLad guidance and notebook references refreshed. |
| Double-blind package | ✅ Ready | `make em-submission` verified; flat archive produced. |
| Preprint | ✅ Ready | `make preprint` generates EarthArXiv cover + manuscript bundle. |
| Cover letter | ✅ Ready | Portal text version finalised (dated 2 November 2025; EarthArXiv preprint disclosed). |
| ORCID & metadata | ✅ Ready | ORCID recorded on title page; submission metadata summarised in `submission-metadata.md`. |
| Final proofing | ✅ Ready | Spellcheck, linting, and clean `make repro` runs completed for both manuscripts. |

### Immediate Next Steps
1. Perform final proofing pass: spellcheck, reference formatting check, repo lint/clean builds.
2. Execute fresh `make dbhdistfit-truncdata-repro` and `make dbhdistfit-hps-repro`, archiving outputs for records.
3. Assemble submission artefacts (em-submission.zip, cover-letter text, title page) and launch FS portal upload.
