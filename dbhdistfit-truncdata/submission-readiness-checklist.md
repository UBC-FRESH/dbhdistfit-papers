## Submission Readiness Checklist (Draft)

| Category | Status | Notes |
| --- | --- | --- |
| Article scope | ⚠️ In Progress | Narrative refresh nearly complete; target journal confirmation outstanding. |
| Data pipeline | ✅ Ready | Fixed-area preprocessing rebuilt around legacy PSP pickle (`scripts/preprocess_data.py`). |
| Figures & tables | ✅ Ready | Regenerated after data refresh via `scripts/generate_figures.py` / `generate_tables.py`. |
| Manuscript formatting | ⚠️ In Progress | LaTeX build clean; need journal style audit once venue is locked. |
| Word count block | ✅ Ready | Automated via `manuscript/scripts/wordcount.sh` and populated in `main.tex`. |
| Statements & Declarations | ✅ Ready | Funding, employment, and data statements updated in `main.tex`. |
| Data availability | ⚠️ In Progress | In-text GitHub reference added; README/DataLad instructions still to update. |
| Double-blind package | ✅ Ready | `make em-submission` verified; flat archive produced. |
| Preprint | ✅ Ready | `make preprint` generates EarthArXiv cover + manuscript bundle. |
| Cover letter | ⚠️ Pending | Tailor journal metadata once submission venue is locked. |
| ORCID & metadata | ⚠️ Pending | Confirm portal requirements prior to submission. |
| Final proofing | ⚠️ Pending | Word count, linting, and QA to run at finalisation. |

### Immediate Next Steps
1. Lock target journal and run a style audit (front matter, headings, reference format).
2. Update repository README/DataLad instructions to match the manuscript’s GitHub reference and note weighting guidance.
3. Draft cover-letter boilerplate and collect ORCID/metadata details ahead of portal entry.
