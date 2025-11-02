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
| Double-blind package | ⚠️ Pending | Run and verify `scripts/prepare_em_submission.py` once manuscript stabilises. |
| Preprint | ⚠️ Pending | Build EarthArXiv PDF after manuscript text is finalised. |
| Cover letter | ⚠️ Pending | Tailor journal metadata once submission venue is locked. |
| ORCID & metadata | ⚠️ Pending | Confirm portal requirements prior to submission. |
| Final proofing | ⚠️ Pending | Word count, linting, and QA to run at finalisation. |

### Immediate Next Steps
1. Finish porting legacy material (narrative polish + appendix cross-check) and refresh citations/references.
2. Validate tables/figures against the original notebook and document any deviations in the discussion.
3. Add reproducibility notebook plus EM/preprint packaging tests before submission tooling.
