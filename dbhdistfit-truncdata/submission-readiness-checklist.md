## Submission Readiness Checklist (Draft)

| Category | Status | Notes |
| --- | --- | --- |
| Article scope | ⚠️ In Progress | Legacy text partially ported; final narrative and target journal still to confirm. |
| Data pipeline | ✅ Ready | Fixed-area preprocessing implemented (`scripts/preprocess_data.py`). |
| Figures & tables | ✅ Ready | Automated via `scripts/generate_figures.py` and `scripts/generate_tables.py`. |
| Manuscript formatting | ⚠️ In Progress | Forest Science styling to confirm once target journal locked; current draft compiles cleanly. |
| Word count block | ✅ Ready | Automated via `manuscript/scripts/wordcount.sh` and populated in `main.tex`. |
| Statements & Declarations | ✅ Ready | Funding, employment, and data statements updated in `main.tex`. |
| Data availability | ⚠️ In Progress | Reference GitHub/DataLad workflow in manuscript and README. |
| Double-blind package | ✅ Ready | `make em-submission` verified; flat archive produced. |
| Preprint | ✅ Ready | `make preprint` generates EarthArXiv cover + manuscript bundle. |
| Cover letter | ⚠️ Pending | Tailor journal metadata once submission venue is locked. |
| ORCID & metadata | ⚠️ Pending | Confirm portal requirements prior to submission. |
| Final proofing | ⚠️ Pending | Word count, linting, and QA to run at finalisation. |

### Immediate Next Steps
1. Finalise narrative polish while maintaining the brief word limit (currently 1\,877 words including references).
2. Expand data availability text to document DataLad workflow and external PSP data access procedures.
3. Update legacy citations/appendix mathematics as needed, then begin polishing title-page/cover-letter content for Forest Science submission.
